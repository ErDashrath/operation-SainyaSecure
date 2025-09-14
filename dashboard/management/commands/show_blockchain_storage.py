from django.core.management.base import BaseCommand
from blockchain.models import BlockchainTransaction
from p2p_sync.models import LocalLedgerBlock
from messaging.models import Message
from users.models import Device
import json


class Command(BaseCommand):
    help = 'Show current blockchain ledger records and storage locations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed record information',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔗 OPERATION SainyaSecure - BLOCKCHAIN STORAGE REPORT'))
        self.stdout.write('=' * 70)

        # Database location
        from django.conf import settings
        db_path = settings.DATABASES['default']['NAME']
        self.stdout.write(f'📍 Database Location: {db_path}')
        self.stdout.write('')

        # Master Blockchain Ledger
        self.stdout.write(self.style.WARNING('🏛️ MASTER BLOCKCHAIN LEDGER (blockchain_blockchaintransaction)'))
        master_txs = BlockchainTransaction.objects.all().order_by('-timestamp')
        self.stdout.write(f'Total Records: {master_txs.count()}')
        
        if master_txs.exists():
            self.stdout.write('Recent Transactions:')
            for tx in master_txs[:5]:
                status = '🟢 Synced' if tx.is_synced else '🟡 Pending'
                self.stdout.write(f'  • {tx.tx_hash[:16]}... | {tx.sender} → {tx.receiver} | {status}')
                if options['detailed']:
                    self.stdout.write(f'    Block: {tx.block_id} | Lamport: {tx.lamport_clock} | Time: {tx.timestamp}')
        else:
            self.stdout.write('  ⚠️ No master ledger records found')
        self.stdout.write('')

        # Local P2P Mini-Ledgers
        self.stdout.write(self.style.WARNING('📱 P2P LOCAL MINI-LEDGERS (p2p_sync_localledgerblock)'))
        local_blocks = LocalLedgerBlock.objects.all().order_by('-timestamp')
        self.stdout.write(f'Total Records: {local_blocks.count()}')
        
        if local_blocks.exists():
            self.stdout.write('Recent Local Blocks:')
            for block in local_blocks[:5]:
                status = '🟢 Synced' if block.is_synced else '🔴 Local Only'
                device_name = block.device.device_id if block.device else 'Unknown'
                self.stdout.write(f'  • {block.block_id} | Device: {device_name} | {status}')
                if options['detailed']:
                    self.stdout.write(f'    Lamport: {block.lamport_clock} | Attempts: {block.sync_attempts} | Time: {block.timestamp}')
        else:
            self.stdout.write('  ⚠️ No local ledger blocks found')
        self.stdout.write('')

        # Message Storage
        self.stdout.write(self.style.WARNING('💬 ENCRYPTED MESSAGES (messaging_message)'))
        messages = Message.objects.all().order_by('-timestamp')
        self.stdout.write(f'Total Records: {messages.count()}')
        
        if messages.exists():
            self.stdout.write('Recent Messages:')
            for msg in messages[:5]:
                anomaly = '🚨 Anomaly' if msg.anomaly_flag else '✅ Clean'
                blockchain_ref = f'TX: {msg.blockchain_tx[:16]}...' if msg.blockchain_tx else 'No TX'
                self.stdout.write(f'  • {msg.msg_id} | {anomaly} | {blockchain_ref}')
                if options['detailed']:
                    sender = msg.sender.device_id if msg.sender else 'Unknown'
                    receiver = msg.receiver.device_id if msg.receiver else 'Unknown'
                    self.stdout.write(f'    {sender} → {receiver} | Payload: {msg.payload[:50]}...')
        else:
            self.stdout.write('  ⚠️ No messages found')
        self.stdout.write('')

        # Device Registry
        self.stdout.write(self.style.WARNING('📡 DEVICE REGISTRY (users_device)'))
        devices = Device.objects.all()
        self.stdout.write(f'Total Devices: {devices.count()}')
        
        if devices.exists():
            self.stdout.write('Registered Devices:')
            for device in devices:
                owner = device.owner.username if device.owner else 'No Owner'
                self.stdout.write(f'  • {device.device_id} | Owner: {owner} | Registered: {device.registered_at}')
        else:
            self.stdout.write('  ⚠️ No devices registered')
        self.stdout.write('')

        # Web3 Status
        self.stdout.write(self.style.WARNING('⛓️ WEB3 BLOCKCHAIN STATUS'))
        try:
            from blockchain.web3_utils import get_web3
            w3 = get_web3()
            self.stdout.write(f'Web3 Connection: 🟡 Demo Mode (not connected to real blockchain)')
            self.stdout.write(f'Smart Contract: 🚧 Not deployed (development phase)')
            self.stdout.write(f'IPFS Integration: 🚧 Not implemented (planned feature)')
        except Exception as e:
            self.stdout.write(f'Web3 Status: 🔴 Not configured - {str(e)}')
        self.stdout.write('')

        # Storage Summary
        self.stdout.write(self.style.SUCCESS('📊 STORAGE SUMMARY'))
        total_blockchain_records = master_txs.count() + local_blocks.count()
        self.stdout.write(f'• Total Blockchain Records: {total_blockchain_records}')
        self.stdout.write(f'• Master Ledger Entries: {master_txs.count()}')
        self.stdout.write(f'• P2P Local Blocks: {local_blocks.count()}')
        self.stdout.write(f'• Encrypted Messages: {messages.count()}')
        self.stdout.write(f'• Registered Devices: {devices.count()}')
        
        synced_count = master_txs.filter(is_synced=True).count()
        sync_percentage = (synced_count / master_txs.count() * 100) if master_txs.count() > 0 else 0
        self.stdout.write(f'• Blockchain Sync Rate: {sync_percentage:.1f}% ({synced_count}/{master_txs.count()})')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🚀 Access blockchain data via:'))
        self.stdout.write('  • Dashboard: http://127.0.0.1:8000/dashboard/')
        self.stdout.write('  • Django Admin: http://127.0.0.1:8000/admin/')
        self.stdout.write('  • GraphQL API: http://127.0.0.1:8000/graphql/')
        self.stdout.write('  • REST API: http://127.0.0.1:8000/api/*/')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('💡 TIP: Run "python manage.py create_demo_data" to populate with sample data'))