from rest_framework import generics, permissions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Message
from .serializers import MessageSerializer

# Send/Receive Message
class MessageListCreateView(generics.ListCreateAPIView):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	permission_classes = [permissions.IsAuthenticated]

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	permission_classes = [permissions.IsAuthenticated]

# Fetch messages by peer/user
class MessagesByPeerView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        peer_id = self.kwargs.get('peer_id')
        return Message.objects.filter(sender__device_id=peer_id) | Message.objects.filter(receiver__device_id=peer_id)

# P2P Message Handling
from rest_framework.views import APIView
from rest_framework.response import Response

class SendP2PMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        """Send message in P2P offline mode"""
        from p2p_sync.p2p_comm import p2p_manager
        from users.models import Device
        
        sender_device_id = request.data.get('sender_device_id')
        receiver_peer_id = request.data.get('receiver_peer_id')
        message_payload = request.data.get('payload')
        
        try:
            sender_device = Device.objects.get(device_id=sender_device_id)
            result = p2p_manager.send_p2p_message(sender_device, receiver_peer_id, message_payload)
            return Response(result)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


# Simple API for form submissions
@csrf_exempt
@require_POST
def send_message_api(request):
    """Enhanced API for sending messages between devices"""
    try:
        from users.models import Device
        import json
        import uuid
        import random
        
        # Get form data with new field names
        sender_device_id = request.POST.get('sender_device') or request.POST.get('device') or 'device_001'
        receiver_device_id = request.POST.get('receiver_device') or sender_device_id
        message_text = request.POST.get('message', '')
        encrypt = request.POST.get('encrypt') == 'on'
        priority = request.POST.get('priority') == 'on'
        
        if not message_text:
            return JsonResponse({'success': False, 'error': 'Message content is required'})
        
        if not sender_device_id or not receiver_device_id:
            return JsonResponse({'success': False, 'error': 'Both sender and receiver devices are required'})
        
        # Create or get sender device
        sender_device, created = Device.objects.get_or_create(
            device_id=sender_device_id,
            defaults={
                'owner_id': 1,  # Default user
                'public_key': f'mock_key_{sender_device_id}',
                'device_name': f'Device {sender_device_id.upper()}',
                'clearance_level': random.choice([2, 3, 4, 5])
            }
        )
        
        # Create or get receiver device (or handle broadcast)
        if receiver_device_id == 'BROADCAST':
            receiver_device = sender_device  # For broadcast, use sender as placeholder
        else:
            receiver_device, created = Device.objects.get_or_create(
                device_id=receiver_device_id,
                defaults={
                    'owner_id': 1,  # Default user
                    'public_key': f'mock_key_{receiver_device_id}',
                    'device_name': f'Device {receiver_device_id.upper()}',
                    'clearance_level': random.choice([2, 3, 4, 5])
                }
            )
        
        # Generate unique message ID
        msg_id = f'msg_{uuid.uuid4().hex[:12]}'
        
        # Prepare message payload (encrypt if requested)
        if encrypt:
            # Simulate encryption by modifying payload
            payload = f'[ENCRYPTED] {message_text} [/ENCRYPTED]'
        else:
            payload = message_text
        
        # Create message with available fields only
        message = Message.objects.create(
            msg_id=msg_id,
            payload=payload,
            sender=sender_device,
            receiver=receiver_device,
            anomaly_flag=random.choice([True, False]) if random.random() < 0.15 else False,  # 15% chance of anomaly
            blockchain_tx=f'tx_{uuid.uuid4().hex[:16]}'
        )
        
        # Log to blockchain if priority message
        if priority:
            try:
                from blockchain.models import MasterLedger
                import datetime
                
                ledger_entry = MasterLedger.objects.create(
                    tx_hash=f'{uuid.uuid4().hex}',
                    timestamp=datetime.datetime.now(),
                    from_device_id=sender_device_id,
                    to_device_id=receiver_device_id,
                    mode_when_created='normal',
                    is_resync=False
                )
            except Exception as e:
                print(f"Blockchain logging failed: {e}")
        
        return JsonResponse({
            'success': True,
            'msg_id': message.msg_id,
            'from_device': sender_device_id,
            'to_device': receiver_device_id,
            'timestamp': message.timestamp.isoformat(),
            'encrypted': encrypt,
            'priority': priority,
            'is_anomaly': message.anomaly_flag,
            'blockchain_logged': priority
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def message_list_api(request):
    """Simple API for getting message list"""
    try:
        limit = int(request.GET.get('limit', 20))
        messages = Message.objects.order_by('-timestamp')[:limit]
        
        message_data = []
        for msg in messages:
            message_data.append({
                'id': msg.id,
                'msg_id': msg.msg_id,
                'payload': msg.payload[:100] + '...' if len(msg.payload) > 100 else msg.payload,
                'timestamp': msg.timestamp.isoformat(),
                'sender': msg.sender.device_id,
                'receiver': msg.receiver.device_id,
                'anomaly_flag': msg.anomaly_flag
            })
        
        return JsonResponse({'messages': message_data})
        
    except Exception as e:
        return JsonResponse({'error': str(e)})

@csrf_exempt
def message_stats_api(request):
    """Simple API for message statistics"""
    try:
        total_messages = Message.objects.count()
        anomaly_count = Message.objects.filter(anomaly_flag=True).count()
        recent_count = Message.objects.filter(
            timestamp__gte=timezone.now() - timezone.timedelta(hours=24)
        ).count()
        
        return JsonResponse({
            'total_messages': total_messages,
            'anomaly_count': anomaly_count,
            'recent_24h': recent_count,
            'anomaly_rate': round((anomaly_count / total_messages * 100), 2) if total_messages > 0 else 0
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)})

# Web view for message list
def message_list_view(request):
    """Display message list page"""
    from django.shortcuts import render
    from datetime import timedelta
    
    messages = Message.objects.select_related('sender', 'receiver').order_by('-timestamp')
    anomaly_count = Message.objects.filter(anomaly_flag=True).count()
    recent_count = Message.objects.filter(
        timestamp__gte=timezone.now() - timedelta(hours=24)
    ).count()
    
    context = {
        'messages': messages,
        'anomaly_count': anomaly_count,
        'recent_count': recent_count,
        'total_count': messages.count(),
    }
    return render(request, 'messaging/message_list.html', context)
