from rest_framework import generics, permissions
from .models import Device, SoldierProfile
from .serializers import DeviceSerializer, SoldierProfileSerializer

# Device CRUD
class DeviceListCreateView(generics.ListCreateAPIView):
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer
	permission_classes = [permissions.IsAuthenticated]

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer
	permission_classes = [permissions.IsAuthenticated]

# SoldierProfile CRUD
class SoldierProfileListCreateView(generics.ListCreateAPIView):
	queryset = SoldierProfile.objects.all()
	serializer_class = SoldierProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

class SoldierProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = SoldierProfile.objects.all()
	serializer_class = SoldierProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

# TODO: Add JWT/WebAuthn authentication endpoints

# Create your views here.
