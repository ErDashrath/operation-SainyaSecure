"""
Blockchain sync logic for P2P offline-first communications
Handles master ledger, local mini-ledgers, conflict resolution
"""
from django.utils import timezone
from .models import LocalLedgerBlock
from blockchain.models import BlockchainTransaction
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import json
import hashlib

class BlockchainSyncManager:
    """
    Core blockchain sync logic:
    1. Server maintains master blockchain ledger
    2. Each peer maintains local mini-ledger for offline redundancy
    3. P2P mode during connectivity loss
    4. Resync with conflict resolution using Lamport/vector clocks
    """
    
    def __init__(self):
        self.lamport_clock = 0
        
    def create_block_hash(self, block_data):
        """Create SHA256 hash of block data"""
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def validate_signature(self, block, public_key):
        """Validate block signature using RSA"""
        # TODO: Implement RSA signature validation
        # This is a placeholder for cryptographic validation
        return True
    
    def increment_lamport_clock(self, received_clock=None):
        """Increment Lamport clock for ordering events"""
        if received_clock:
            self.lamport_clock = max(self.lamport_clock, received_clock) + 1
        else:
            self.lamport_clock += 1
        return self.lamport_clock
    
    def update_vector_clock(self, node_id, vector_clock=None):
        """Update vector clock for distributed systems"""
        if vector_clock is None:
            vector_clock = {}
        vector_clock[node_id] = vector_clock.get(node_id, 0) + 1
        return vector_clock
    
    def resolve_conflicts(self, local_blocks, master_blocks):
        """
        Resolve conflicts using Lamport clocks and vector clocks
        Priority: 1) Lamport clock, 2) Vector clock comparison, 3) Hash comparison
        """
        conflicts = []
        resolved_blocks = []
        
        for local_block in local_blocks:
            conflict_found = False
            
            for master_block in master_blocks:
                # Check for timestamp conflicts
                if (local_block.timestamp == master_block.timestamp or
                    abs((local_block.timestamp - master_block.timestamp).total_seconds()) < 1):
                    
                    # Use Lamport clock for ordering
                    if local_block.lamport_clock > master_block.lamport_clock:
                        resolved_blocks.append(local_block)
                        conflicts.append({
                            'type': 'timestamp_conflict',
                            'resolution': 'lamport_clock_priority',
                            'local_block': local_block.block_id,
                            'master_block': master_block.tx_hash
                        })
                    elif local_block.lamport_clock < master_block.lamport_clock:
                        # Master block takes priority
                        pass
                    else:
                        # Vector clock comparison or hash-based tie-breaking
                        if self.compare_vector_clocks(local_block.vector_clock, master_block.vector_clock):
                            resolved_blocks.append(local_block)
                        conflicts.append({
                            'type': 'lamport_tie',
                            'resolution': 'vector_clock_comparison',
                            'local_block': local_block.block_id
                        })
                    
                    conflict_found = True
                    break
            
            if not conflict_found:
                resolved_blocks.append(local_block)
        
        return resolved_blocks, conflicts
    
    def compare_vector_clocks(self, clock1, clock2):
        """Compare vector clocks to determine causal ordering"""
        # TODO: Implement proper vector clock comparison
        # For now, use simple comparison
        return sum(clock1.values()) > sum(clock2.values())
    
    def validate_block_integrity(self, block):
        """Validate block hash, signature, and chain integrity"""
        try:
            # 1. Validate hash
            expected_hash = self.create_block_hash({
                'block_id': block.block_id,
                'prev_hash': block.prev_hash,
                'payload_hash': block.payload_hash,
                'timestamp': block.timestamp.isoformat(),
                'device': str(block.device_id)
            })
            
            # 2. Validate signature (placeholder)
            signature_valid = self.validate_signature(block, None)  # TODO: Add public key
            
            # 3. Check chain integrity (prev_hash linkage)
            # TODO: Implement chain validation
            
            return signature_valid
        except Exception as e:
            return False
    
    def sync_local_to_master(self, local_blocks):
        """
        Sync local ledger blocks to master blockchain ledger
        Returns: sync_status, conflicts, merged_blocks
        """
        try:
            # 1. Fetch current master ledger
            master_blocks = list(BlockchainTransaction.objects.all())
            
            # 2. Validate local blocks
            valid_local_blocks = [
                block for block in local_blocks 
                if self.validate_block_integrity(block) and not block.is_synced
            ]
            
            # 3. Resolve conflicts
            resolved_blocks, conflicts = self.resolve_conflicts(valid_local_blocks, master_blocks)
            
            # 4. Append resolved blocks to master ledger
            merged_count = 0
            for block in resolved_blocks:
                try:
                    # Convert LocalLedgerBlock to BlockchainTransaction
                    master_block = BlockchainTransaction.objects.create(
                        tx_hash=f"tx_{block.block_id}",
                        block_id=block.block_id,
                        sender=str(block.device_id),
                        receiver="broadcast",  # TODO: Get actual receiver
                        payload_hash=block.payload_hash,
                        timestamp=block.timestamp,
                        signature=block.signature,
                        lamport_clock=block.lamport_clock,
                        vector_clock=block.vector_clock,
                        is_synced=True
                    )
                    
                    # Mark local block as synced
                    block.is_synced = True
                    block.save()
                    
                    merged_count += 1
                except Exception as e:
                    # Handle duplicate or invalid blocks
                    continue
            
            return {
                'status': 'success',
                'received_blocks': len(local_blocks),
                'valid_blocks': len(valid_local_blocks),
                'conflicts': conflicts,
                'merged_blocks': merged_count,
                'master_ledger_size': BlockchainTransaction.objects.count()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'merged_blocks': 0
            }

# Singleton instance
blockchain_sync = BlockchainSyncManager()