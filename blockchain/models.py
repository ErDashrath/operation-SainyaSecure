from django.db import models

class BlockchainTransaction(models.Model):
    """Master blockchain ledger - central server maintains this"""
    tx_hash = models.CharField(max_length=128, unique=True)
    block_id = models.CharField(max_length=128)
    sender = models.CharField(max_length=128)
    receiver = models.CharField(max_length=128)
    payload_hash = models.CharField(max_length=128)
    timestamp = models.DateTimeField()
    signature = models.TextField()
    lamport_clock = models.IntegerField(default=0)  # For conflict resolution
    vector_clock = models.JSONField(default=dict)   # For distributed ordering
    is_synced = models.BooleanField(default=False)  # Track sync status# Create your models here.
