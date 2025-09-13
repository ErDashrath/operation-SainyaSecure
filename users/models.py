from django.db import models

class Device(models.Model):
	device_id = models.CharField(max_length=128, unique=True)
	owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	public_key = models.TextField()
	registered_at = models.DateTimeField(auto_now_add=True)

class SoldierProfile(models.Model):
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
	rank = models.CharField(max_length=64)
	unit = models.CharField(max_length=128)
	device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True)

# Create your models here.
