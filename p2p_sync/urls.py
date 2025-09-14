from django.urls import path
from . import views

app_name = 'p2p_sync'

urlpatterns = [
    # Web views
    path('', views.p2p_status_view, name='p2p_status'),
    path('dashboard/', views.p2p_status_view, name='p2p_dashboard'),
    
    # Main P2P views
    path('blocks/', views.LocalLedgerBlockListCreateView.as_view(), name='ledger-block-list-create'),
    path('blocks/<int:pk>/', views.LocalLedgerBlockDetailView.as_view(), name='ledger-block-detail'),
    path('sync_ledger/', views.ResyncLedgerView.as_view(), name='sync-ledger'),
    path('status/', views.P2PStatusView.as_view(), name='status'),
    path('sync/', views.ManualSyncView.as_view(), name='manual_sync'),
    path('switch_offline/', views.SwitchOfflineView.as_view(), name='switch-offline'),
    path('switch_online/', views.SwitchOnlineView.as_view(), name='switch-online'),
    
    # Enhanced API endpoints
    path('api/status/', views.p2p_status_api, name='api_status'),
    path('api/toggle/', views.toggle_p2p_mode, name='api_toggle'),
    path('api/discover/', views.peer_discovery_api, name='api_discover'),
    path('api/sync/', views.sync_with_peers_api, name='api_sync'),
    path('api/send-message/', views.send_p2p_message_api, name='api_send_message'),
]