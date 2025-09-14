from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import AnomalyAlert
from .serializers import AnomalyAlertSerializer
from messaging.models import Message

# Anomaly alert CRUD
class AnomalyAlertListCreateView(generics.ListCreateAPIView):
    queryset = AnomalyAlert.objects.all()
    serializer_class = AnomalyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

class AnomalyAlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnomalyAlert.objects.all()
    serializer_class = AnomalyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

# Fetch flagged messages
class FlaggedMessagesView(generics.ListAPIView):
    serializer_class = AnomalyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnomalyAlert.objects.filter(alert_type__in=['spoofed_id', 'malicious_content', 'abnormal_pattern'])

# AI Analysis endpoints
class AnalyzeMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Analyze a message for anomalies using AI"""
        message_id = request.data.get('message_id')
        if not message_id:
            return Response({'error': 'message_id required'}, status=400)
        
        try:
            message = Message.objects.get(id=message_id)
            
            # Mock AI analysis - in production this would call actual AI models
            analysis_result = self._analyze_message(message)
            
            # Create anomaly alert if suspicious
            if analysis_result['is_anomaly']:
                alert = AnomalyAlert.objects.create(
                    message=message,
                    alert_type=analysis_result['alert_type'],
                    explanation=analysis_result['explanation']
                )
                
                # Flag the message
                message.anomaly_flag = True
                message.save()
                
                return Response({
                    'anomaly_detected': True,
                    'alert_id': alert.id,
                    'alert_type': alert.alert_type,
                    'explanation': alert.explanation
                })
            else:
                return Response({
                    'anomaly_detected': False,
                    'confidence': analysis_result['confidence']
                })
                
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=404)
    
    def _analyze_message(self, message):
        """Mock AI analysis function"""
        import random
        
        # Mock analysis patterns
        suspicious_keywords = ['attack', 'bomb', 'classified', 'secret']
        payload_lower = message.payload.lower()
        
        has_suspicious_content = any(keyword in payload_lower for keyword in suspicious_keywords)
        
        # Random anomaly detection for demo
        is_anomaly = has_suspicious_content or random.random() < 0.1
        
        if is_anomaly:
            if has_suspicious_content:
                return {
                    'is_anomaly': True,
                    'alert_type': 'malicious_content',
                    'explanation': 'Message contains suspicious keywords indicating potential security threat',
                    'confidence': 0.95
                }
            else:
                return {
                    'is_anomaly': True,
                    'alert_type': 'abnormal_pattern',
                    'explanation': 'Communication pattern deviates from normal behavior',
                    'confidence': 0.75
                }
        else:
            return {
                'is_anomaly': False,
                'confidence': 0.98
            }

class AnomalyStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get anomaly detection statistics"""
        total_alerts = AnomalyAlert.objects.count()
        flagged_messages = Message.objects.filter(anomaly_flag=True).count()
        total_messages = Message.objects.count()
        
        # Get alerts by type
        alert_types = AnomalyAlert.objects.values('alert_type').distinct()
        type_counts = {}
        for alert_type in alert_types:
            count = AnomalyAlert.objects.filter(alert_type=alert_type['alert_type']).count()
            type_counts[alert_type['alert_type']] = count
        
        return Response({
            'total_alerts': total_alerts,
            'flagged_messages': flagged_messages,
            'total_messages': total_messages,
            'detection_rate': (flagged_messages / total_messages * 100) if total_messages > 0 else 0,
            'alert_types': type_counts
        })

class RecentAnomaliesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get recent anomaly alerts"""
        limit = request.query_params.get('limit', 10)
        alerts = AnomalyAlert.objects.order_by('-detected_at')[:int(limit)]
        
        alert_data = []
        for alert in alerts:
            alert_data.append({
                'id': alert.id,
                'message_id': alert.message.msg_id,
                'alert_type': alert.alert_type,
                'explanation': alert.explanation,
                'detected_at': alert.detected_at,
                'sender': alert.message.sender.device_id,
                'receiver': alert.message.receiver.device_id
            })
        
        return Response({'recent_anomalies': alert_data})

# Simple API functions
@csrf_exempt
def anomaly_stats_api(request):
    """Simple API for anomaly statistics"""
    try:
        total_alerts = AnomalyAlert.objects.count()
        flagged_messages = Message.objects.filter(anomaly_flag=True).count()
        total_messages = Message.objects.count()
        
        return JsonResponse({
            'total_alerts': total_alerts,
            'flagged_messages': flagged_messages,
            'total_messages': total_messages,
            'detection_rate': round((flagged_messages / total_messages * 100), 2) if total_messages > 0 else 0
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})

@csrf_exempt
@require_POST
def analyze_message_api(request):
    """Simple API for message analysis"""
    try:
        message_id = request.POST.get('message_id')
        if not message_id:
            return JsonResponse({'success': False, 'error': 'Message ID required'})
        
        # Mock analysis for demo
        import random
        is_anomaly = random.random() < 0.3
        
        return JsonResponse({
            'success': True,
            'anomaly_detected': is_anomaly,
            'confidence': round(random.uniform(0.7, 0.98), 2),
            'alert_type': 'abnormal_pattern' if is_anomaly else None
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
