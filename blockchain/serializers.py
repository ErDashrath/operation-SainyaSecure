from rest_framework import serializers
from .models import BlockchainTransaction

class BlockchainTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockchainTransaction
        fields = '__all__'

# Serializers for legacy blockchain tables (used via raw SQL)
class MasterLedgerSerializer(serializers.Serializer):
    """Serializer for blockchain_masterledger table data"""
    tx_hash = serializers.CharField(max_length=64)
    message_hash = serializers.CharField(max_length=64)
    timestamp = serializers.DateTimeField()
    lamport_clock = serializers.IntegerField()
    mode_when_created = serializers.CharField(max_length=10)
    is_resync = serializers.BooleanField()
    local_ledger_hash = serializers.CharField(max_length=64)
    block_hash = serializers.CharField(max_length=64)
    from_device_id = serializers.IntegerField()
    to_device_id = serializers.IntegerField()

class CommandCenterSerializer(serializers.Serializer):
    """Serializer for blockchain_commandcenter table data"""
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField()
    current_mode = serializers.CharField(max_length=10)
    master_ledger_hash = serializers.CharField(max_length=64)
    global_lamport_clock = serializers.IntegerField()
    last_resync = serializers.DateTimeField()
    created_at = serializers.DateTimeField()

class DeviceStatusSerializer(serializers.Serializer):
    """Serializer for blockchain_device table data"""
    id = serializers.IntegerField()
    device_id = serializers.CharField(max_length=50)
    device_type = serializers.CharField(max_length=20)
    is_authorized = serializers.BooleanField()
    is_online = serializers.BooleanField()
    clearance_level = serializers.IntegerField()
    last_sync = serializers.DateTimeField()
    local_ledger_count = serializers.IntegerField()
    local_lamport_clock = serializers.IntegerField()

class ModeChangeLogSerializer(serializers.Serializer):
    """Serializer for blockchain_modechangelog table data"""
    id = serializers.IntegerField()
    old_mode = serializers.CharField(max_length=10)
    new_mode = serializers.CharField(max_length=10)
    changed_by = serializers.CharField(max_length=50)
    timestamp = serializers.DateTimeField()
    reason = serializers.CharField(allow_blank=True)

class LocalLedgerSerializer(serializers.Serializer):
    """Serializer for blockchain_localledger table data"""
    id = serializers.IntegerField()
    tx_hash = serializers.CharField(max_length=64)
    from_device_id = serializers.CharField(max_length=50)
    to_device_id = serializers.CharField(max_length=50)
    message_hash = serializers.CharField(max_length=64)
    timestamp = serializers.DateTimeField()
    local_lamport_clock = serializers.IntegerField()
    is_synced = serializers.BooleanField()
    created_offline = serializers.BooleanField()
    sync_timestamp = serializers.DateTimeField(allow_null=True)
    device_id = serializers.IntegerField()
