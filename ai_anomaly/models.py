from django.db import models

class AnomalyAlert(models.Model):
	message = models.ForeignKey('messaging.Message', on_delete=models.CASCADE)
	alert_type = models.CharField(max_length=64)
	explanation = models.TextField()
	detected_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
