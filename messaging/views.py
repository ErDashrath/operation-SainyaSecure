from rest_framework import generics, permissions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
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
    """Simple API for sending messages from HTML forms"""
    try:
        from users.models import Device
        import json
        
        device_id = request.POST.get('device') or 'device_001'
        message_text = request.POST.get('message', '')
        
        if not message_text:
            return JsonResponse({'success': False, 'error': 'Message is required'})
        
        # Create or get device
        device, created = Device.objects.get_or_create(
            device_id=device_id,
            defaults={
                'owner_id': 1,  # Default user
                'public_key': f'mock_key_{device_id}',
            }
        )
        
        # Create message
        message = Message.objects.create(
            msg_id=f'msg_{len(Message.objects.all()) + 1}',
            payload=message_text,
            sender=device,
            receiver=device,  # Self for demo
        )
        
        return JsonResponse({
            'success': True,
            'message_id': message.msg_id,
            'timestamp': message.timestamp.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
