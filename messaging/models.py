from django.db import models

class Message(models.Model):
	msg_id = models.CharField(max_length=128, unique=True)
	sender = models.ForeignKey('users.Device', on_delete=models.CASCADE, related_name='sent_messages')
	receiver = models.ForeignKey('users.Device', on_delete=models.CASCADE, related_name='received_messages')
	payload = models.TextField()  # Encrypted
	timestamp = models.DateTimeField(auto_now_add=True)
	blockchain_tx = models.CharField(max_length=128, null=True, blank=True)  # Blockchain tx hash
	anomaly_flag = models.BooleanField(default=False)

# Create your models here.
