from django.urls import path
from . import views
from .views import (
    BlockchainTransactionListCreateView, BlockchainTransactionDetailView, 
    ValidateBlockView, CommandCenterStatusView, SwitchModeView,
    BlockchainStatsView, RecentTransactionsView
)

app_name = 'blockchain'

urlpatterns = [
    # Transaction endpoints
    path('', BlockchainTransactionListCreateView.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', BlockchainTransactionDetailView.as_view(), name='blockchain-tx-detail'),
    path('validate/', ValidateBlockView.as_view(), name='validate-block'),
    
    # Web views
    path('list/', views.transaction_list_view, name='transaction_list_view'),
    
    # Command center and mode management
    path('command-center/', CommandCenterStatusView.as_view(), name='command-center-status'),
    path('switch-mode/', SwitchModeView.as_view(), name='switch-mode'),
    
    # Statistics and monitoring
    path('stats/', BlockchainStatsView.as_view(), name='blockchain-stats'),
    path('recent/', RecentTransactionsView.as_view(), name='recent-transactions'),
    
    # API endpoints for forms/AJAX
    path('api/stats/', views.blockchain_stats_api, name='api_stats'),
    path('api/switch-mode/', views.switch_mode_api, name='api_switch_mode'),
]
