from rest_framework import generics, permissions
from .models import AnomalyAlert
from .serializers import AnomalyAlertSerializer

# Anomaly alert CRUD
class AnomalyAlertListCreateView(generics.ListCreateAPIView):
    queryset = AnomalyAlert.objects.all()
    serializer_class = AnomalyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

class AnomalyAlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnomalyAlert.objects.all()
    serializer_class = AnomalyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

# Fetch flagged messages
class FlaggedMessagesView(generics.ListAPIView):
    serializer_class = AnomalyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnomalyAlert.objects.filter(alert_type__in=['spoofed_id', 'malicious_content', 'abnormal_pattern'])
