from django.urls import path
from . import views
from .views import MessageListCreateView, MessageDetailView, MessagesByPeerView

app_name = 'messaging'

urlpatterns = [
    path('', MessageListCreateView.as_view(), name='message_list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('peer/<str:peer_id>/', MessagesByPeerView.as_view(), name='messages-by-peer'),
    # P2P messaging
    path('send_p2p/', views.SendP2PMessageView.as_view(), name='send-p2p-message'),
    # API endpoints
    path('api/send/', views.send_message_api, name='api_send'),
]
