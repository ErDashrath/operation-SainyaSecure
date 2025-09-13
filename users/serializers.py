from rest_framework import serializers
from .models import Device, SoldierProfile

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class SoldierProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldierProfile
        fields = '__all__'
