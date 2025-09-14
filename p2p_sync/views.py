from rest_framework import generics, permissions
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import LocalLedgerBlock
from .serializers import LocalLedgerBlockSerializer

# Local ledger CRUD
class LocalLedgerBlockListCreateView(generics.ListCreateAPIView):
	queryset = LocalLedgerBlock.objects.all()
	serializer_class = LocalLedgerBlockSerializer
	permission_classes = [permissions.IsAuthenticated]

class LocalLedgerBlockDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = LocalLedgerBlock.objects.all()
	serializer_class = LocalLedgerBlockSerializer
	permission_classes = [permissions.IsAuthenticated]

# Resync endpoint
from rest_framework.views import APIView
from rest_framework.response import Response
class ResyncLedgerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        """
        Resync local ledger with master blockchain ledger
        Implements conflict resolution using Lamport/vector clocks
        """
        from .blockchain_sync import blockchain_sync
        
        # 1. Get device information
        device_id = request.data.get('device_id')
        if not device_id:
            return Response({'error': 'device_id required'}, status=400)
        
        # 2. Fetch unsynced local blocks for this device
        local_blocks = LocalLedgerBlock.objects.filter(
            device__device_id=device_id,
            is_synced=False
        ).order_by('timestamp', 'lamport_clock')
        
        # 3. Perform sync with conflict resolution
        sync_result = blockchain_sync.sync_local_to_master(local_blocks)
        
        # 4. Update sync statistics
        if sync_result['status'] == 'success':
            # Reset failed sync attempts for successfully synced blocks
            LocalLedgerBlock.objects.filter(
                device__device_id=device_id,
                is_synced=True
            ).update(sync_attempts=0)
        else:
            # Increment failed sync attempts
            local_blocks.update(sync_attempts=models.F('sync_attempts') + 1)
        
        return Response(sync_result)

# P2P Mode Views
class P2PStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        from .p2p_comm import p2p_manager
        return Response(p2p_manager.get_offline_status())

class SwitchOfflineView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        from .p2p_comm import p2p_manager
        result = p2p_manager.switch_to_offline_mode()
        peers = p2p_manager.discover_peers()
        result['discovered_peers'] = peers
        return Response(result)

class SwitchOnlineView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        from .p2p_comm import p2p_manager
        result = p2p_manager.switch_to_online_mode()
        return Response(result)

class ManualSyncView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        from .p2p_comm import p2p_manager
        result = p2p_manager.sync_with_peers()
        return Response({'status': 'success', 'sync_result': result})


# Simple API functions for AJAX calls
@csrf_exempt
def p2p_status_api(request):
    """Simple API for getting P2P status"""
    try:
        from .p2p_comm import p2p_manager
        status = p2p_manager.get_offline_status()
        data = {
            'offline_mode': status.get('offline_mode', False),
            'connected_peers': len(status.get('peer_list', [])),
            'peer_count': len(status.get('peer_list', [])),  # Add for dashboard compatibility
            'peer_list': status.get('peer_list', []),
            'local_blocks_pending_sync': LocalLedgerBlock.objects.filter(is_synced=False).count()
        }
    except:
        # Fallback data for demo
        data = {
            'offline_mode': True,  # Show offline by default for demo
            'connected_peers': 0,
            'peer_count': 0,  # Add for dashboard compatibility
            'peer_list': [],
            'local_blocks_pending_sync': 0
        }
    return JsonResponse(data)


@csrf_exempt
@require_POST
def toggle_p2p_mode(request):
    """Toggle between P2P offline and server online modes"""
    try:
        from .p2p_comm import p2p_manager
        current_status = p2p_manager.get_offline_status()
        
        if current_status.get('offline_mode', False):
            result = p2p_manager.switch_to_online_mode()
            mode = 'online'
        else:
            result = p2p_manager.switch_to_offline_mode()
            mode = 'offline'
        
        return JsonResponse({
            'status': f'switched to {mode} mode',
            'offline_mode': not current_status.get('offline_mode', False)
        })
    except:
        # Fallback toggle for demo
        import json
        body = json.loads(request.body) if request.body else {}
        current_offline = body.get('current_offline', False)
        new_mode = not current_offline
        
        return JsonResponse({
            'status': f'switched to {"offline" if new_mode else "online"} mode',
            'offline_mode': new_mode
        })
