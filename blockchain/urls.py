from django.urls import path
from . import views
from .views import BlockchainTransactionListCreateView, BlockchainTransactionDetailView, ValidateBlockView

app_name = 'blockchain'

urlpatterns = [
    path('', BlockchainTransactionListCreateView.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', BlockchainTransactionDetailView.as_view(), name='blockchain-tx-detail'),
    path('validate_block/', ValidateBlockView.as_view(), name='validate-block'),
]
