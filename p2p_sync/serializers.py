from rest_framework import serializers
from .models import LocalLedgerBlock

class LocalLedgerBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalLedgerBlock
        fields = '__all__'
