from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count
from messaging.models import Message
from users.models import Device
from blockchain.models import BlockchainTransaction
from p2p_sync.models import LocalLedgerBlock
from ai_anomaly.models import AnomalyAlert
import sqlite3

# Dashboard endpoints
class DashboardSummaryView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		# Aggregate messages, blocks, alerts, connectivity status
		summary_data = {
			'messages': {
				'total': Message.objects.count(),
				'recent_24h': Message.objects.filter(timestamp__gte=timezone.now() - timezone.timedelta(hours=24)).count(),
				'anomalies': Message.objects.filter(anomaly_flag=True).count()
			},
			'blockchain': {
				'transactions': BlockchainTransaction.objects.count(),
				'local_blocks': LocalLedgerBlock.objects.count(),
				'pending_sync': LocalLedgerBlock.objects.filter(is_synced=False).count()
			},
			'devices': {
				'total': Device.objects.count(),
				'active': Device.objects.count(),  # Mock - all devices as active
				'online': 0  # Mock - no real-time status yet
			},
			'alerts': {
				'total': AnomalyAlert.objects.count(),
				'recent': AnomalyAlert.objects.filter(detected_at__gte=timezone.now() - timezone.timedelta(hours=24)).count()
			}
		}
		return Response({'summary': summary_data})

# Audit replay timeline
class AuditReplayView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		# Return timeline of past messages/blocks
		try:
			conn = sqlite3.connect('db.sqlite3')
			cursor = conn.cursor()
			
			# Get combined timeline from messages and blockchain entries
			cursor.execute("""
				SELECT 'message' as type, msg_id as id, timestamp, sender_id, receiver_id, anomaly_flag
				FROM messaging_message
				UNION ALL
				SELECT 'blockchain' as type, tx_hash as id, timestamp, from_device_id, to_device_id, NULL
				FROM blockchain_masterledger
				ORDER BY timestamp DESC
				LIMIT 50
			""")
			
			timeline_data = []
			for row in cursor.fetchall():
				timeline_data.append({
					'type': row[0],
					'id': row[1],
					'timestamp': row[2],
					'from': row[3],
					'to': row[4],
					'anomaly': row[5] if row[5] is not None else False
				})
			
			conn.close()
			return Response({'timeline': timeline_data})
		except Exception as e:
			return Response({'timeline': [], 'error': str(e)})

class SystemStatusView(APIView):
	permission_classes = [IsAuthenticated]
	
	def get(self, request):
		"""Get overall system status"""
		try:
			conn = sqlite3.connect('db.sqlite3')
			cursor = conn.cursor()
			
			# Command center status
			cursor.execute("SELECT name, current_mode, is_active, global_lamport_clock FROM blockchain_commandcenter")
			cc = cursor.fetchone()
			
			# Device status counts
			cursor.execute("SELECT is_online, COUNT(*) FROM blockchain_device GROUP BY is_online")
			device_status = dict(cursor.fetchall())
			
			# Recent activity
			cursor.execute("SELECT COUNT(*) FROM messaging_message WHERE timestamp > datetime('now', '-1 hour')")
			recent_messages = cursor.fetchone()[0]
			
			conn.close()
			
			return Response({
				'command_center': {
					'name': cc[0] if cc else 'Unknown',
					'mode': cc[1] if cc else 'normal',
					'active': cc[2] if cc else False,
					'clock': cc[3] if cc else 0
				},
				'devices': {
					'online': device_status.get(1, 0),
					'offline': device_status.get(0, 0)
				},
				'activity': {
					'recent_messages': recent_messages
				}
			})
		except Exception as e:
			return Response({'error': str(e)})

def landing_page(request):
    """Landing page for Operation SainyaSecure"""
    return render(request, 'landing.html')

class DashboardHomeView(TemplateView):
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get summary statistics
        context['message_count'] = Message.objects.count()
        context['blockchain_count'] = BlockchainTransaction.objects.count()
        context['device_count'] = Device.objects.count()
        
        # Get recent data
        context['recent_messages'] = Message.objects.order_by('-timestamp')[:5]
        context['recent_transactions'] = BlockchainTransaction.objects.order_by('-timestamp')[:5]
        context['devices'] = Device.objects.all()
        
        return context

def dashboard_home(request):
    """Simple function-based view for dashboard home"""
    import sqlite3
    from django.utils import timezone
    
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Get basic counts
        context = {
            'message_count': Message.objects.count(),
            'blockchain_count': BlockchainTransaction.objects.count(),
            'device_count': Device.objects.count(),
            'recent_messages': Message.objects.select_related('sender', 'receiver').order_by('-timestamp')[:5],
            'devices': Device.objects.all(),
        }
        
        # Get recent blockchain transactions with device info from master ledger
        cursor.execute("""
            SELECT tx_hash, timestamp, from_device_id, to_device_id, mode_when_created, is_resync, 'blockchain' as block_type
            FROM blockchain_masterledger 
            ORDER BY timestamp DESC 
            LIMIT 5
        """)
        
        recent_transactions = []
        for row in cursor.fetchall():
            recent_transactions.append({
                'tx_hash': row[0],
                'timestamp': row[1],
                'from_device_id': row[2] if row[2] else 'SYSTEM',
                'to_device_id': row[3] if row[3] else 'ALL',
                'mode': row[4] or 'normal',
                'is_synced': not row[5],  # is_resync=True means not synced
                'block_type': row[6] or 'message'
            })
        
        context['recent_transactions'] = recent_transactions
        
        # Get system activity with real device communications
        cursor.execute("""
            SELECT 
                'message' as type,
                m.timestamp,
                s.device_id as from_device,
                r.device_id as to_device,
                m.anomaly_flag,
                m.msg_id,
                m.blockchain_tx
            FROM messaging_message m
            JOIN users_device s ON m.sender_id = s.id
            JOIN users_device r ON m.receiver_id = r.id
            ORDER BY m.timestamp DESC
            LIMIT 10
        """)
        
        system_activities = []
        for row in cursor.fetchall():
            system_activities.append({
                'type': 'Message',
                'timestamp': row[1],
                'from_device': row[2],
                'to_device': row[3],
                'status': 'Anomaly' if row[4] else 'Secure',
                'details': f"{row[2]} → {row[3]}",
                'hash': row[6] if row[6] else 'No Hash',
                'msg_id': row[5]
            })
        
        # Add blockchain activities
        cursor.execute("""
            SELECT 
                'blockchain' as type,
                timestamp,
                from_device_id,
                to_device_id,
                is_resync,
                tx_hash,
                mode_when_created
            FROM blockchain_masterledger
            ORDER BY timestamp DESC
            LIMIT 5
        """)
        
        for row in cursor.fetchall():
            system_activities.append({
                'type': 'Blockchain',
                'timestamp': row[1],
                'from_device': row[2] if row[2] else 'SYSTEM',
                'to_device': row[3] if row[3] else 'ALL',
                'status': 'Resync' if row[4] else 'Normal',
                'details': f"{row[2] or 'SYSTEM'} → {row[3] or 'ALL'}",
                'hash': row[5][:16] + '...' if row[5] else 'No Hash',
                'mode': row[6] or 'normal'
            })
        
        # Sort all activities by timestamp
        system_activities.sort(key=lambda x: x['timestamp'], reverse=True)
        context['system_activities'] = system_activities[:8]  # Show latest 8 activities
        
        conn.close()
        
    except Exception as e:
        print(f"Dashboard error: {e}")
        # Fallback to basic data
        context = {
            'message_count': Message.objects.count(),
            'blockchain_count': BlockchainTransaction.objects.count(),
            'device_count': Device.objects.count(),
            'recent_messages': Message.objects.select_related('sender', 'receiver').order_by('-timestamp')[:5],
            'recent_transactions': [],
            'devices': Device.objects.all(),
            'system_activities': [],
            'error': str(e)
        }
    
    return render(request, 'dashboard/home.html', context)

# Simple API functions
@csrf_exempt
def dashboard_stats_api(request):
    """Simple API for dashboard statistics"""
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Get various counts
        cursor.execute("SELECT COUNT(*) FROM messaging_message")
        message_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM messaging_message WHERE anomaly_flag = 1")
        anomaly_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM blockchain_masterledger")
        blockchain_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users_device")
        device_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT current_mode FROM blockchain_commandcenter")
        current_mode = cursor.fetchone()
        
        conn.close()
        
        return JsonResponse({
            'messages': message_count,
            'anomalies': anomaly_count,
            'blockchain_entries': blockchain_count,
            'devices': device_count,
            'current_mode': current_mode[0] if current_mode else 'normal',
            'system_status': 'operational'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})

@csrf_exempt
def system_activity_api(request):
    """API for fetching real-time system activity with filtering"""
    try:
        import sqlite3
        
        # Get filter parameters
        from_device = request.GET.get('from_device', '')
        to_device = request.GET.get('to_device', '')
        activity_type = request.GET.get('type', '')
        
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        activities = []
        
        # Build dynamic WHERE clauses for filtering
        message_where = "WHERE 1=1"
        blockchain_where = "WHERE 1=1"
        
        if from_device:
            message_where += f" AND m.sender_device = '{from_device}'"
            blockchain_where += f" AND bl.from_device_id = '{from_device}'"
        
        if to_device:
            message_where += f" AND m.recipient_device = '{to_device}'"
            blockchain_where += f" AND bl.to_device_id = '{to_device}'"
        
        # Get message activities with content
        if not activity_type or activity_type == 'Message' or activity_type == 'Anomaly':
            cursor.execute(f"""
                SELECT 
                    m.timestamp,
                    sd.device_id as sender_device,
                    rd.device_id as receiver_device,
                    m.anomaly_flag,
                    m.msg_id,
                    m.payload,
                    m.blockchain_tx
                FROM messaging_message m
                LEFT JOIN users_device sd ON m.sender_id = sd.id
                LEFT JOIN users_device rd ON m.receiver_id = rd.id
                WHERE 1=1
                {f"AND sd.device_id = '{from_device}'" if from_device else ''}
                {f"AND rd.device_id = '{to_device}'" if to_device else ''}
                {'AND m.anomaly_flag = 1' if activity_type == 'Anomaly' else ''}
                ORDER BY m.timestamp DESC
                LIMIT 10
            """)
            
            for row in cursor.fetchall():
                activities.append({
                    'type': 'Message',
                    'timestamp': row[0],
                    'from_device': row[1] if row[1] else 'SYSTEM',
                    'to_device': row[2] if row[2] else 'BROADCAST',
                    'status': 'Anomaly' if row[3] else 'Secure',
                    'hash': row[6][:8] + '...' if row[6] else f'msg_{row[4][:8]}...',
                    'msg_id': row[4],
                    'content': row[5][:50] + '...' if row[5] and len(row[5]) > 50 else row[5] or 'ENCRYPTED',
                    'anomaly_type': None
                })
        
        # Get blockchain activities
        if not activity_type or activity_type == 'Blockchain':
            cursor.execute(f"""
                SELECT 
                    bl.timestamp,
                    bl.from_device_id,
                    bl.to_device_id,
                    bl.is_resync,
                    bl.tx_hash,
                    bl.mode_when_created
                FROM blockchain_masterledger bl
                WHERE 1=1
                {f"AND bl.from_device_id = '{from_device}'" if from_device else ''}
                {f"AND bl.to_device_id = '{to_device}'" if to_device else ''}
                ORDER BY bl.timestamp DESC
                LIMIT 10
            """)
            
            for row in cursor.fetchall():
                activities.append({
                    'type': 'Blockchain',
                    'timestamp': row[0],
                    'from_device': str(row[1]) if row[1] else 'COMMAND_CENTER',
                    'to_device': str(row[2]) if row[2] else 'ALL_UNITS',
                    'status': 'Synced' if not row[3] else 'Resync',
                    'hash': row[4][:8] + '...' if row[4] else 'No Hash',
                    'mode': row[5] or 'normal',
                    'content': 'BLOCKCHAIN_TRANSACTION'
                })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Add filter info to response
        filter_info = {
            'from_device': from_device,
            'to_device': to_device,
            'activity_type': activity_type,
            'active_filters': bool(from_device or to_device or activity_type)
        }
        
        conn.close()
        
        return JsonResponse({
            'activities': activities[:15],
            'timestamp': timezone.now().isoformat(),
            'filter_info': filter_info
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e), 'activities': [], 'filter_info': {}})
