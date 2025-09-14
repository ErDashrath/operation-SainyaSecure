from django.urls import path
from . import views
from .views import MessageListCreateView, MessageDetailView, MessagesByPeerView, SendP2PMessageView

app_name = 'messaging'

urlpatterns = [
    # Message CRUD
    path('', MessageListCreateView.as_view(), name='message_list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('peer/<str:peer_id>/', MessagesByPeerView.as_view(), name='messages-by-peer'),
    
    # Web views
    path('list/', views.message_list_view, name='message_list_view'),
    
    # P2P messaging
    path('send-p2p/', SendP2PMessageView.as_view(), name='send-p2p-message'),
    
    # API endpoints for forms/AJAX
    path('api/send/', views.send_message_api, name='api_send'),
    path('api/list/', views.message_list_api, name='api_list'),
    path('api/stats/', views.message_stats_api, name='api_stats'),
]
