from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender_device_id = serializers.CharField(source='sender.device_id', read_only=True)
    receiver_device_id = serializers.CharField(source='receiver.device_id', read_only=True)
    sender_owner = serializers.CharField(source='sender.owner.username', read_only=True)
    receiver_owner = serializers.CharField(source='receiver.owner.username', read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'

class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new messages"""
    class Meta:
        model = Message
        fields = ['msg_id', 'payload', 'sender', 'receiver', 'blockchain_tx']

class MessageSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for message summaries"""
    sender_device_id = serializers.CharField(source='sender.device_id', read_only=True)
    receiver_device_id = serializers.CharField(source='receiver.device_id', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'msg_id', 'timestamp', 'anomaly_flag', 'sender_device_id', 'receiver_device_id']
