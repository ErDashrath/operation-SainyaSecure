from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Web UI
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard_home, name='home'),
    
    # API endpoints
    path('summary/', views.DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('audit-replay/', views.AuditReplayView.as_view(), name='audit-replay'),
    path('system-status/', views.SystemStatusView.as_view(), name='system-status'),
    
    # Simple API functions
    path('api/stats/', views.dashboard_stats_api, name='api_stats'),
    path('api/activity/', views.system_activity_api, name='api_activity'),
]
