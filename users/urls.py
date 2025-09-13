from django.urls import path
from . import views

from .views import DeviceListCreateView, DeviceDetailView, SoldierProfileListCreateView, SoldierProfileDetailView

urlpatterns = [
    path('devices/', DeviceListCreateView.as_view(), name='device-list-create'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('soldiers/', SoldierProfileListCreateView.as_view(), name='soldier-list-create'),
    path('soldiers/<int:pk>/', SoldierProfileDetailView.as_view(), name='soldier-detail'),
    # TODO: Add JWT/WebAuthn endpoints
]
