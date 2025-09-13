from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard_home, name='home'),
    path('summary/', views.DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('audit_replay/', views.AuditReplayView.as_view(), name='audit-replay'),
]
