"""
P2P Communication Manager for offline mode
Handles direct peer-to-peer communication when server is unavailable
"""
from django.utils import timezone
from .models import LocalLedgerBlock
from .blockchain_sync import blockchain_sync
import json
import hashlib

class P2PCommManager:
    """
    Manages direct P2P communications in offline mode:
    1. Direct radio/Wi-Fi communication between peers
    2. Local blockchain ledger logging
    3. Append-only, signed transaction logging
    """
    
    def __init__(self):
        self.is_offline_mode = False
        self.connected_peers = set()
    
    def switch_to_offline_mode(self):
        """Switch to P2P offline mode when server is unreachable"""
        self.is_offline_mode = True
        return {
            'status': 'offline_mode_enabled',
            'p2p_mode': True,
            'server_reachable': False
        }
    
    def switch_to_online_mode(self):
        """Switch back to server mode when connectivity restored"""
        self.is_offline_mode = False
        return {
            'status': 'online_mode_enabled',
            'p2p_mode': False,
            'server_reachable': True
        }
    
    def discover_peers(self):
        """
        Discover nearby peers for P2P communication
        TODO: Implement actual peer discovery (Wi-Fi Direct, Bluetooth, etc.)
        """
        # Placeholder for peer discovery logic
        mock_peers = [
            {'peer_id': 'peer_001', 'ip': '192.168.1.101', 'status': 'online'},
            {'peer_id': 'peer_002', 'ip': '192.168.1.102', 'status': 'online'}
        ]
        
        for peer in mock_peers:
            self.connected_peers.add(peer['peer_id'])
        
        return mock_peers
    
    def send_p2p_message(self, sender_device, receiver_peer_id, message_payload):
        """
        Send message directly to peer in offline mode
        Log transaction in local blockchain ledger
        """
        try:
            # 1. Create message hash
            message_data = {
                'sender': sender_device.device_id,
                'receiver': receiver_peer_id,
                'payload': message_payload,
                'timestamp': timezone.now().isoformat()
            }
            payload_hash = hashlib.sha256(
                json.dumps(message_data, sort_keys=True).encode()
            ).hexdigest()
            
            # 2. Create local ledger block
            prev_block = LocalLedgerBlock.objects.filter(
                device=sender_device
            ).order_by('-timestamp').first()
            
            prev_hash = prev_block.payload_hash if prev_block else "genesis"
            
            # 3. Generate signature (placeholder)
            signature = f"sig_{payload_hash[:16]}"  # TODO: Implement actual RSA signing
            
            # 4. Create blockchain entry with Lamport clock
            lamport_clock = blockchain_sync.increment_lamport_clock()
            vector_clock = blockchain_sync.update_vector_clock(sender_device.device_id)
            
            block = LocalLedgerBlock.objects.create(
                block_id=f"block_{payload_hash[:16]}",
                prev_hash=prev_hash,
                payload_hash=payload_hash,
                signature=signature,
                device=sender_device,
                lamport_clock=lamport_clock,
                vector_clock=vector_clock,
                is_synced=False  # Will sync when back online
            )
            
            # 5. Attempt P2P transmission (placeholder)
            transmission_result = self.transmit_to_peer(receiver_peer_id, message_data)
            
            return {
                'status': 'p2p_message_sent',
                'block_id': block.block_id,
                'payload_hash': payload_hash,
                'lamport_clock': lamport_clock,
                'transmission_success': transmission_result
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def transmit_to_peer(self, peer_id, message_data):
        """
        Actual P2P transmission (radio/Wi-Fi Direct)
        TODO: Implement actual transmission protocol
        """
        if peer_id in self.connected_peers:
            # Simulate successful transmission
            return True
        return False
    
    def receive_p2p_message(self, receiver_device, message_data):
        """
        Receive message from peer in offline mode
        Validate and log in local blockchain ledger
        """
        try:
            # 1. Validate message integrity
            expected_hash = hashlib.sha256(
                json.dumps(message_data, sort_keys=True).encode()
            ).hexdigest()
            
            if expected_hash != message_data.get('payload_hash'):
                return {'status': 'error', 'error': 'hash_mismatch'}
            
            # 2. Create local ledger entry for received message
            prev_block = LocalLedgerBlock.objects.filter(
                device=receiver_device
            ).order_by('-timestamp').first()
            
            prev_hash = prev_block.payload_hash if prev_block else "genesis"
            
            # 3. Update clocks
            received_lamport = message_data.get('lamport_clock', 0)
            lamport_clock = blockchain_sync.increment_lamport_clock(received_lamport)
            vector_clock = blockchain_sync.update_vector_clock(receiver_device.device_id)
            
            # 4. Log received message
            block = LocalLedgerBlock.objects.create(
                block_id=f"recv_{expected_hash[:16]}",
                prev_hash=prev_hash,
                payload_hash=expected_hash,
                signature=message_data.get('signature', ''),
                device=receiver_device,
                lamport_clock=lamport_clock,
                vector_clock=vector_clock,
                is_synced=False
            )
            
            return {
                'status': 'p2p_message_received',
                'block_id': block.block_id,
                'lamport_clock': lamport_clock
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_offline_status(self):
        """Get current P2P/offline status"""
        return {
            'offline_mode': self.is_offline_mode,
            'connected_peers': len(self.connected_peers),
            'peer_list': list(self.connected_peers),
            'local_blocks_pending_sync': LocalLedgerBlock.objects.filter(
                is_synced=False
            ).count()
        }

# Singleton instance
p2p_manager = P2PCommManager()