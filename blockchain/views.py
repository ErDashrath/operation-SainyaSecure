from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import BlockchainTransaction
from .serializers import BlockchainTransactionSerializer
import sqlite3

# Blockchain transaction CRUD
class BlockchainTransactionListCreateView(generics.ListCreateAPIView):
	queryset = BlockchainTransaction.objects.all()
	serializer_class = BlockchainTransactionSerializer
	permission_classes = [permissions.IsAuthenticated]

class BlockchainTransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = BlockchainTransaction.objects.all()
	serializer_class = BlockchainTransactionSerializer
	permission_classes = [permissions.IsAuthenticated]

# Block validation placeholder
class ValidateBlockView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request):
		from .web3_utils import submit_block, validate_block
		block_data = request.data.get('block')
		valid = validate_block(block_data)
		if valid:
			tx_hash = submit_block(block_data)
			# TODO: Trigger async Celery task for blockchain write
			return Response({'status': 'block validated', 'tx_hash': tx_hash})
		else:
			return Response({'status': 'invalid block'}, status=400)

# Command Center and Mode Management
class CommandCenterStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get command center status and operational mode"""
        try:
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            
            # Get command center status
            cursor.execute("SELECT name, current_mode, is_active, global_lamport_clock FROM blockchain_commandcenter")
            cc = cursor.fetchone()
            
            # Get device statuses
            cursor.execute("SELECT device_id, device_type, is_authorized, is_online, clearance_level FROM blockchain_device")
            devices = cursor.fetchall()
            
            # Get recent mode changes
            cursor.execute("""
                SELECT old_mode, new_mode, changed_by, timestamp, reason 
                FROM blockchain_modechangelog 
                ORDER BY timestamp DESC LIMIT 5
            """)
            mode_changes = cursor.fetchall()
            
            conn.close()
            
            return Response({
                'command_center': {
                    'name': cc[0] if cc else 'Unknown',
                    'current_mode': cc[1] if cc else 'normal',
                    'is_active': cc[2] if cc else False,
                    'global_clock': cc[3] if cc else 0
                },
                'devices': [
                    {
                        'device_id': d[0],
                        'type': d[1],
                        'authorized': d[2],
                        'online': d[3],
                        'clearance': d[4]
                    } for d in devices
                ],
                'recent_mode_changes': [
                    {
                        'old_mode': m[0],
                        'new_mode': m[1],
                        'changed_by': m[2],
                        'timestamp': m[3],
                        'reason': m[4]
                    } for m in mode_changes
                ]
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class SwitchModeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Switch operational mode (normal/offline/resync)"""
        new_mode = request.data.get('mode')
        reason = request.data.get('reason', '')
        changed_by = request.data.get('changed_by', 'SYSTEM')
        
        if new_mode not in ['normal', 'offline', 'resync']:
            return Response({'error': 'Invalid mode'}, status=400)
        
        try:
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            
            # Get current mode
            cursor.execute("SELECT current_mode FROM blockchain_commandcenter")
            current_mode = cursor.fetchone()[0]
            
            # Update mode
            cursor.execute("""
                UPDATE blockchain_commandcenter 
                SET current_mode = ?, global_lamport_clock = global_lamport_clock + 1
            """, (new_mode,))
            
            # Log mode change
            cursor.execute("""
                INSERT INTO blockchain_modechangelog 
                (old_mode, new_mode, changed_by, timestamp, reason)
                VALUES (?, ?, ?, datetime('now'), ?)
            """, (current_mode, new_mode, changed_by, reason))
            
            conn.commit()
            conn.close()
            
            return Response({
                'status': 'mode switched',
                'old_mode': current_mode,
                'new_mode': new_mode,
                'changed_by': changed_by
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class BlockchainStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get blockchain statistics"""
        try:
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            
            # Get transaction counts
            cursor.execute("SELECT COUNT(*) FROM blockchain_blockchaintransaction")
            tx_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM blockchain_masterledger")
            master_ledger_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM blockchain_localledger WHERE is_synced = 0")
            pending_sync = cursor.fetchone()[0]
            
            # Get transactions by mode
            cursor.execute("""
                SELECT mode_when_created, COUNT(*) 
                FROM blockchain_masterledger 
                GROUP BY mode_when_created
            """)
            mode_stats = cursor.fetchall()
            
            conn.close()
            
            return Response({
                'blockchain_transactions': tx_count,
                'master_ledger_entries': master_ledger_count,
                'pending_sync': pending_sync,
                'transactions_by_mode': {mode[0]: mode[1] for mode in mode_stats}
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class RecentTransactionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get recent blockchain transactions"""
        limit = request.query_params.get('limit', 10)
        
        try:
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT tx_hash, from_device_id, to_device_id, timestamp, mode_when_created
                FROM blockchain_masterledger 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (int(limit),))
            
            transactions = cursor.fetchall()
            conn.close()
            
            tx_data = []
            for tx in transactions:
                tx_data.append({
                    'tx_hash': tx[0],
                    'from_device': tx[1],
                    'to_device': tx[2],
                    'timestamp': tx[3],
                    'mode': tx[4]
                })
            
            return Response({'recent_transactions': tx_data})
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# Simple API functions
@csrf_exempt
def blockchain_stats_api(request):
    """Simple API for blockchain statistics"""
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM blockchain_masterledger")
        ledger_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT current_mode FROM blockchain_commandcenter")
        current_mode = cursor.fetchone()[0]
        
        conn.close()
        
        return JsonResponse({
            'ledger_entries': ledger_count,
            'current_mode': current_mode,
            'status': 'operational'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})

# Web view for blockchain transaction list
def transaction_list_view(request):
    """Display comprehensive blockchain transaction list with military operations data"""
    from django.shortcuts import render
    
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Get all messaging communications with blockchain tracking
        cursor.execute("""
            SELECT 
                m.id as message_id,
                m.message_id as msg_hash,
                m.timestamp, 
                m.sender_device, 
                m.recipient_device, 
                m.content,
                m.is_anomaly,
                m.encrypted_payload,
                m.anomaly_type,
                bl.tx_hash,
                bl.mode as blockchain_mode,
                bl.is_synced,
                d1.device_name as from_device_name,
                d2.device_name as to_device_name,
                d1.clearance_level as from_clearance,
                d2.clearance_level as to_clearance
            FROM messaging_message m
            LEFT JOIN blockchain_masterledger bl ON m.id = bl.message_id
            LEFT JOIN users_device d1 ON m.sender_device = d1.device_id
            LEFT JOIN users_device d2 ON m.recipient_device = d2.device_id
            ORDER BY m.timestamp DESC
            LIMIT 50
        """)
        
        transactions = []
        for row in cursor.fetchall():
            # Determine security level based on content and clearance
            security_level = "STANDARD"
            from_clearance = row[14] or 1
            to_clearance = row[15] or 1
            max_clearance = max(from_clearance, to_clearance)
            
            if max_clearance >= 5:
                security_level = "TOP_SECRET"
            elif max_clearance >= 4:
                security_level = "CLASSIFIED" 
            elif max_clearance >= 3:
                security_level = "RESTRICTED"
            elif max_clearance >= 2:
                security_level = "CONFIDENTIAL"
            
            # Determine validation status
            validation_status = "VERIFIED"
            if row[6]:  # is_anomaly
                validation_status = "ANOMALY_DETECTED"
            elif row[9] and not row[11]:  # has blockchain entry but not synced
                validation_status = "PENDING_VALIDATION"
            elif not row[9]:  # no blockchain entry
                validation_status = "NOT_LOGGED"
            
            # Use blockchain tx_hash if available, otherwise use message hash
            tx_hash = row[9] if row[9] else f"msg_{row[1]}"
            
            transactions.append({
                'tx_hash': tx_hash,
                'message_id': row[0],
                'timestamp': row[2],
                'from_device_id': row[3] if row[3] else 'SYSTEM',
                'to_device_id': row[4] if row[4] else 'BROADCAST',
                'from_device_name': row[12] if row[12] else row[3],
                'to_device_name': row[13] if row[13] else row[4],
                'content': row[5] if row[5] else 'ENCRYPTED_PAYLOAD',
                'operational_mode': row[10] if row[10] else 'NORMAL',
                'is_synced': row[11] if row[11] is not None else False,
                'block_type': 'MESSAGE',
                'security_level': security_level,
                'validation_status': validation_status,
                'is_anomaly': row[6] or False,
                'anomaly_type': row[8] if row[8] else None,
                'is_encrypted': bool(row[7]),
                'from_clearance': from_clearance,
                'to_clearance': to_clearance,
                'has_blockchain_entry': bool(row[9])
            })
        
        # Get command center operational status
        cursor.execute("""
            SELECT name, current_mode, is_active, global_lamport_clock, 
                   authority_level, emergency_protocols_active
            FROM blockchain_commandcenter
        """)
        cc_row = cursor.fetchone()
        command_center = {
            'name': cc_row[0] if cc_row else 'OPERATION_TRINETRA_CC',
            'current_mode': cc_row[1] if cc_row else 'NORMAL',
            'is_active': cc_row[2] if cc_row else True,
            'global_lamport_clock': cc_row[3] if cc_row else 0,
            'authority_level': cc_row[4] if cc_row and len(cc_row) > 4 else 'COMMAND',
            'emergency_active': cc_row[5] if cc_row and len(cc_row) > 5 else False
        }
        
        # Get blockchain integrity metrics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_blocks,
                COUNT(CASE WHEN is_synced = 0 THEN 1 END) as pending_sync,
                COUNT(CASE WHEN mode = 'emergency' THEN 1 END) as emergency_blocks,
                COUNT(CASE WHEN block_type = 'COMMAND' THEN 1 END) as command_blocks
            FROM blockchain_masterledger
        """)
        stats_row = cursor.fetchone()
        
        # Get device authentication status
        cursor.execute("""
            SELECT 
                COUNT(*) as total_devices,
                COUNT(CASE WHEN is_authenticated = 1 THEN 1 END) as authenticated,
                COUNT(CASE WHEN is_online = 1 THEN 1 END) as online,
                COUNT(CASE WHEN clearance_level >= 4 THEN 1 END) as high_clearance
            FROM users_device
        """)
        device_stats = cursor.fetchone()
        
        # Get recent anomalies
        cursor.execute("""
            SELECT m.id, m.sender_device, m.recipient_device, m.timestamp, m.anomaly_type
            FROM messaging_message m
            WHERE m.is_anomaly = 1
            ORDER BY m.timestamp DESC
            LIMIT 5
        """)
        anomalies = cursor.fetchall()
        
        conn.close()
        
        context = {
            'transactions': transactions,
            'command_center': command_center,
            'blockchain_stats': {
                'total_blocks': stats_row[0] if stats_row else 0,
                'pending_sync': stats_row[1] if stats_row else 0,
                'emergency_blocks': stats_row[2] if stats_row else 0,
                'command_blocks': stats_row[3] if stats_row else 0,
            },
            'device_stats': {
                'total_devices': device_stats[0] if device_stats else 0,
                'authenticated': device_stats[1] if device_stats else 0,
                'online': device_stats[2] if device_stats else 0,
                'high_clearance': device_stats[3] if device_stats else 0,
            },
            'recent_anomalies': [
                {
                    'id': a[0],
                    'sender': a[1],
                    'recipient': a[2], 
                    'timestamp': a[3],
                    'type': a[4]
                } for a in anomalies
            ] if anomalies else []
        }
        return render(request, 'blockchain/transaction_list.html', context)
        
    except Exception as e:
        context = {
            'transactions': [],
            'command_center': {'name': 'ERROR', 'current_mode': 'UNKNOWN', 'is_active': False, 'global_lamport_clock': 0},
            'blockchain_stats': {'total_blocks': 0, 'pending_sync': 0, 'emergency_blocks': 0, 'command_blocks': 0},
            'device_stats': {'total_devices': 0, 'authenticated': 0, 'online': 0, 'high_clearance': 0},
            'recent_anomalies': [],
            'error': str(e)
        }
        return render(request, 'blockchain/transaction_list.html', context)

@csrf_exempt
@require_POST
def switch_mode_api(request):
    """Simple API for mode switching"""
    try:
        new_mode = request.POST.get('mode', 'normal')
        reason = request.POST.get('reason', 'Manual switch')
        
        # Mock mode switch for demo
        return JsonResponse({
            'success': True,
            'new_mode': new_mode,
            'message': f'Switched to {new_mode} mode'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Create your views here.
