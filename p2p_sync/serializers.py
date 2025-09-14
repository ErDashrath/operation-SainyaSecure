from rest_framework import serializers
from .models import LocalLedgerBlock

class LocalLedgerBlockSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(source='device.device_id', read_only=True)
    device_owner = serializers.CharField(source='device.owner.username', read_only=True)
    
    class Meta:
        model = LocalLedgerBlock
        fields = '__all__'

class P2PStatusSerializer(serializers.Serializer):
    """Serializer for P2P status information"""
    offline_mode = serializers.BooleanField()
    connected_peers = serializers.IntegerField()
    peer_list = serializers.ListField(child=serializers.CharField())
    local_blocks_pending_sync = serializers.IntegerField()
    last_sync_time = serializers.DateTimeField(allow_null=True)
    network_quality = serializers.CharField(max_length=20)

class SyncResultSerializer(serializers.Serializer):
    """Serializer for sync operation results"""
    status = serializers.CharField(max_length=20)
    synced_blocks = serializers.IntegerField()
    failed_blocks = serializers.IntegerField()
    conflicts_resolved = serializers.IntegerField()
    sync_time = serializers.DateTimeField()
    errors = serializers.ListField(child=serializers.CharField(), required=False)
