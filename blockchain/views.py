from rest_framework import generics, permissions
from .models import BlockchainTransaction
from .serializers import BlockchainTransactionSerializer

# Blockchain transaction CRUD
class BlockchainTransactionListCreateView(generics.ListCreateAPIView):
	queryset = BlockchainTransaction.objects.all()
	serializer_class = BlockchainTransactionSerializer
	permission_classes = [permissions.IsAuthenticated]

class BlockchainTransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = BlockchainTransaction.objects.all()
	serializer_class = BlockchainTransactionSerializer
	permission_classes = [permissions.IsAuthenticated]

# Block validation placeholder
from rest_framework.views import APIView
from rest_framework.response import Response
class ValidateBlockView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request):
		from .web3_utils import submit_block, validate_block
		block_data = request.data.get('block')
		valid = validate_block(block_data)
		if valid:
			tx_hash = submit_block(block_data)
			# TODO: Trigger async Celery task for blockchain write
			return Response({'status': 'block validated', 'tx_hash': tx_hash})
		else:
			return Response({'status': 'invalid block'}, status=400)

# Create your views here.
