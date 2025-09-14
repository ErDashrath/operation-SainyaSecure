from django.urls import path
from .views import (
    AnomalyAlertListCreateView, AnomalyAlertDetailView, FlaggedMessagesView,
    AnalyzeMessageView, AnomalyStatsView, RecentAnomaliesView
)
from . import views

app_name = 'ai_anomaly'

urlpatterns = [
    # Anomaly alert CRUD
    path('alerts/', AnomalyAlertListCreateView.as_view(), name='anomaly-alert-list-create'),
    path('alerts/<int:pk>/', AnomalyAlertDetailView.as_view(), name='anomaly-alert-detail'),
    
    # Flagged content
    path('flagged/', FlaggedMessagesView.as_view(), name='flagged-messages'),
    
    # AI analysis
    path('analyze/', AnalyzeMessageView.as_view(), name='analyze-message'),
    path('stats/', AnomalyStatsView.as_view(), name='anomaly-stats'),
    path('recent/', RecentAnomaliesView.as_view(), name='recent-anomalies'),
    
    # API endpoints for forms/AJAX
    path('api/stats/', views.anomaly_stats_api, name='api_stats'),
    path('api/analyze/', views.analyze_message_api, name='api_analyze'),
]
