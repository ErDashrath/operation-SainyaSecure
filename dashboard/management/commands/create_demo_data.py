from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Device
from messaging.models import Message
from blockchain.models import BlockchainTransaction
from p2p_sync.models import LocalLedgerBlock
from datetime import datetime, timedelta
import uuid
import random


class Command(BaseCommand):
    help = 'Create demo data for the military communication system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing demo data first',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing demo data...')
            Device.objects.all().delete()
            Message.objects.all().delete()
            BlockchainTransaction.objects.all().delete()
            LocalLedgerBlock.objects.all().delete()

        # Create demo users
        self.stdout.write('Creating demo users...')
        users = []
        for i in range(3):
            username = f'operator_{i+1:02d}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': f'Operator',
                    'last_name': f'{i+1:02d}',
                    'email': f'{username}@milcomm.mil',
                    'is_active': True
                }
            )
            users.append(user)
            if created:
                self.stdout.write(f'  Created user: {username}')

        # Create demo devices
        self.stdout.write('Creating demo devices...')
        devices = []
        device_names = ['Alpha-Base', 'Bravo-Mobile', 'Charlie-Forward', 'Delta-Command']
        for i, name in enumerate(device_names):
            device_id = f'device_{i+1:03d}'
            public_key = f'-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgk{uuid.uuid4().hex[:40]}\\n-----END PUBLIC KEY-----'
            
            device, created = Device.objects.get_or_create(
                device_id=device_id,
                defaults={
                    'owner': users[i % len(users)],
                    'public_key': public_key,
                }
            )
            devices.append(device)
            if created:
                self.stdout.write(f'  Created device: {device_id} ({name})')

        # Create demo messages
        self.stdout.write('Creating demo messages...')
        message_templates = [
            "Status report: All systems operational",
            "Request backup at coordinates 34.0522, -118.2437",
            "Mission accomplished, returning to base",
            "Enemy movement detected in sector 7",
            "Supply drop scheduled for 1400 hours",
            "Radio check - do you copy?",
            "Evacuation route confirmed via checkpoint Charlie",
            "Weather update: Storm approaching from the west",
            "Patrol completed without incident",
            "Emergency medical assistance required"
        ]
        
        for i in range(15):
            sender = random.choice(devices)
            receiver = random.choice([d for d in devices if d != sender])
            message_text = random.choice(message_templates)
            
            # Create message with timestamp spread over last 24 hours
            created_time = datetime.now() - timedelta(
                hours=random.randint(0, 24),
                minutes=random.randint(0, 59)
            )
            
            msg_id = f'msg_{uuid.uuid4().hex[:12]}'
            blockchain_tx = f'tx_{uuid.uuid4().hex[:16]}'
            
            message = Message.objects.create(
                msg_id=msg_id,
                sender=sender,
                receiver=receiver,
                payload=message_text,
                blockchain_tx=blockchain_tx,
                anomaly_flag=random.choice([False, False, False, True])  # 25% chance of anomaly
            )
            # Manually set the timestamp
            message.timestamp = created_time
            message.save()
            
            self.stdout.write(f'  Created message: {msg_id}')

        # Create demo blockchain transactions
        self.stdout.write('Creating demo blockchain transactions...')
        for i in range(20):
            sender = random.choice(devices)
            receiver = random.choice([d for d in devices if d != sender])
            
            created_time = datetime.now() - timedelta(
                hours=random.randint(0, 48),
                minutes=random.randint(0, 59)
            )
            
            tx_hash = f'0x{uuid.uuid4().hex}'
            block_id = f'block_{i+1:04d}'
            
            transaction = BlockchainTransaction.objects.create(
                tx_hash=tx_hash,
                block_id=block_id,
                sender=sender.device_id,
                receiver=receiver.device_id,
                lamport_clock=i + 1,
                vector_clock=f'{{"device_001": {i}, "device_002": {i+1}}}',
                is_synced=random.choice([True, True, True, False])  # 75% synced
            )
            transaction.timestamp = created_time
            transaction.save()
            
            self.stdout.write(f'  Created blockchain tx: {tx_hash[:16]}...')

        # Create demo local ledger blocks
        self.stdout.write('Creating demo local ledger blocks...')
        for i in range(10):
            device = random.choice(devices)
            
            created_time = datetime.now() - timedelta(
                hours=random.randint(0, 12),
                minutes=random.randint(0, 59)
            )
            
            block_id = f'local_block_{uuid.uuid4().hex[:8]}'
            tx_hash = f'0x{uuid.uuid4().hex}'
            
            local_block = LocalLedgerBlock.objects.create(
                device=device,
                block_id=block_id,
                tx_hash=tx_hash,
                lamport_clock=i + 100,
                vector_clock=f'{{"device_001": {i+50}, "device_002": {i+60}}}',
                is_synced=random.choice([True, False, False])  # 33% synced
            )
            local_block.timestamp = created_time
            local_block.save()
            
            self.stdout.write(f'  Created local block: {block_id}')

        # Summary
        self.stdout.write(self.style.SUCCESS('\\nDemo data creation completed successfully!'))
        self.stdout.write(f'Created:')
        self.stdout.write(f'  - {len(users)} users')
        self.stdout.write(f'  - {Device.objects.count()} devices')
        self.stdout.write(f'  - {Message.objects.count()} messages')
        self.stdout.write(f'  - {BlockchainTransaction.objects.count()} blockchain transactions')
        self.stdout.write(f'  - {LocalLedgerBlock.objects.count()} local ledger blocks')
        self.stdout.write(f'\\nYou can now visit http://127.0.0.1:8000/ to see the dashboard with demo data!')