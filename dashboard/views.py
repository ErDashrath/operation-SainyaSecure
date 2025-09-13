from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Dashboard endpoints
class DashboardSummaryView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		# TODO: Aggregate messages, blocks, alerts, connectivity status
		return Response({'summary': 'dashboard data'})

# Audit replay timeline
class AuditReplayView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		# TODO: Return timeline of past messages/blocks
		return Response({'timeline': []})

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Count
from messaging.models import Message
from users.models import Device
from blockchain.models import BlockchainTransaction
from p2p_sync.models import LocalLedgerBlock


def landing_page(request):
    """Landing page for Operation TRINETRA"""
    return render(request, 'landing.html')


class DashboardHomeView(TemplateView):
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get summary statistics
        context['message_count'] = Message.objects.count()
        context['blockchain_count'] = BlockchainTransaction.objects.count()
        context['device_count'] = Device.objects.count()
        
        # Get recent data
        context['recent_messages'] = Message.objects.order_by('-timestamp')[:5]
        context['recent_transactions'] = BlockchainTransaction.objects.order_by('-timestamp')[:5]
        context['devices'] = Device.objects.all()
        
        return context


def dashboard_home(request):
    """Simple function-based view for dashboard home"""
    context = {
        'message_count': Message.objects.count(),
        'blockchain_count': BlockchainTransaction.objects.count(),
        'device_count': Device.objects.count(),
        'recent_messages': Message.objects.order_by('-timestamp')[:5],
        'recent_transactions': BlockchainTransaction.objects.order_by('-timestamp')[:5],
        'devices': Device.objects.all(),
    }
    return render(request, 'dashboard/home.html', context)
