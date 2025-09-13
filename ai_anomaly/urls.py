from django.urls import path
from .views import AnomalyAlertListCreateView, AnomalyAlertDetailView, FlaggedMessagesView

urlpatterns = [
    path('alerts/', AnomalyAlertListCreateView.as_view(), name='anomaly-alert-list-create'),
    path('alerts/<int:pk>/', AnomalyAlertDetailView.as_view(), name='anomaly-alert-detail'),
    path('flagged/', FlaggedMessagesView.as_view(), name='flagged-messages'),
]
