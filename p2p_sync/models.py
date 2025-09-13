from django.db import models

class LocalLedgerBlock(models.Model):
    """Local mini-ledger - each peer maintains this for offline redundancy"""
    block_id = models.CharField(max_length=128, unique=True)
    prev_hash = models.CharField(max_length=128)
    payload_hash = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)
    signature = models.TextField()
    device = models.ForeignKey('users.Device', on_delete=models.CASCADE)
    lamport_clock = models.IntegerField(default=0)  # For conflict resolution
    vector_clock = models.JSONField(default=dict)   # For distributed ordering
    is_synced = models.BooleanField(default=False)  # Track if synced to master
    sync_attempts = models.IntegerField(default=0)  # Track failed sync attempts# Create your models here.
