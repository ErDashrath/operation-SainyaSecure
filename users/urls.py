from django.urls import path
from . import views

from .views import (
    DeviceListCreateView, DeviceDetailView, DeviceStatusView, DeviceByIdView,
    SoldierProfileListCreateView, SoldierProfileDetailView, 
    UserRegistrationView
)

app_name = 'users'

urlpatterns = [
    # Device endpoints
    path('devices/', DeviceListCreateView.as_view(), name='device-list-create'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('devices/status/', DeviceStatusView.as_view(), name='device-status'),
    path('devices/by-id/<str:device_id>/', DeviceByIdView.as_view(), name='device-by-id'),
    
    # Web views
    path('manage/', views.device_management_view, name='device_management'),
    
    # Soldier profile endpoints
    path('soldiers/', SoldierProfileListCreateView.as_view(), name='soldier-list-create'),
    path('soldiers/<int:pk>/', SoldierProfileDetailView.as_view(), name='soldier-detail'),
    
    # User management
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    
    # API endpoints for forms/AJAX
    path('api/device-status/', views.device_status_api, name='api_device_status'),
    path('api/register-device/', views.register_device_api, name='api_register_device'),
]
