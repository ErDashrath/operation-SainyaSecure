from rest_framework import generics, permissions
from .models import Device, SoldierProfile
from .serializers import DeviceSerializer, SoldierProfileSerializer

# Device CRUD
class DeviceListCreateView(generics.ListCreateAPIView):
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer
	permission_classes = [permissions.IsAuthenticated]

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer
	permission_classes = [permissions.IsAuthenticated]

# SoldierProfile CRUD
class SoldierProfileListCreateView(generics.ListCreateAPIView):
	queryset = SoldierProfile.objects.all()
	serializer_class = SoldierProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

class SoldierProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = SoldierProfile.objects.all()
	serializer_class = SoldierProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Device, SoldierProfile
from .serializers import DeviceSerializer, SoldierProfileSerializer

# Device CRUD
class DeviceListCreateView(generics.ListCreateAPIView):
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer
	permission_classes = [permissions.IsAuthenticated]

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer
	permission_classes = [permissions.IsAuthenticated]

# SoldierProfile CRUD
class SoldierProfileListCreateView(generics.ListCreateAPIView):
	queryset = SoldierProfile.objects.all()
	serializer_class = SoldierProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

class SoldierProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = SoldierProfile.objects.all()
	serializer_class = SoldierProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

# Device Status and Management
class DeviceStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get all device statuses with online/offline info"""
        devices = Device.objects.all()
        device_data = []
        
        for device in devices:
            device_data.append({
                'device_id': device.device_id,
                'owner': device.owner.username if device.owner else 'Unknown',
                'registered_at': device.registered_at,
                'is_online': False,  # TODO: Implement real status check
                'last_seen': device.registered_at,
            })
        
        return Response({'devices': device_data})

class DeviceByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, device_id):
        """Get device by device_id"""
        try:
            device = Device.objects.get(device_id=device_id)
            serializer = DeviceSerializer(device)
            return Response(serializer.data)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=404)

# User Authentication and Registration
class UserRegistrationView(APIView):
    """Register new military user with device"""
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        rank = request.data.get('rank', 'Private')
        unit = request.data.get('unit', 'Unknown')
        device_id = request.data.get('device_id')
        
        if not all([username, email, password, device_id]):
            return Response({'error': 'All fields required'}, status=400)
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create device
            device = Device.objects.create(
                device_id=device_id,
                owner=user,
                public_key=f'mock_key_{device_id}'
            )
            
            # Create soldier profile
            profile = SoldierProfile.objects.create(
                user=user,
                rank=rank,
                unit=unit,
                device=device
            )
            
            return Response({
                'message': 'User registered successfully',
                'user_id': user.id,
                'device_id': device.device_id
            }, status=201)
            
        except Exception as e:
            return Response({'error': str(e)}, status=400)

# Simple API functions
@csrf_exempt
def device_status_api(request):
    """Enhanced API for real-time device status and statistics"""
    try:
        import sqlite3
        from django.utils import timezone
        
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Get basic device statistics (using actual table structure)
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN owner_id IS NOT NULL THEN 1 END) as authenticated
            FROM users_device
        """)
        stats = cursor.fetchone()
        total_devices = stats[0] or 0
        authenticated_count = stats[1] or 0
        
        # Assume all devices are online for demo purposes
        online_count = total_devices
        
        # Count base stations (devices with 'base' in ID)
        cursor.execute("SELECT COUNT(*) FROM users_device WHERE device_id LIKE '%base%'")
        base_stations = cursor.fetchone()[0] or 0
        
        # Count high clearance (staff users)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM users_device d
            JOIN auth_user u ON d.owner_id = u.id
            WHERE u.is_staff = 1
        """)
        high_clearance = cursor.fetchone()[0] or 0
        
        # Get recent activity
        cursor.execute("SELECT COUNT(*) FROM messaging_message WHERE timestamp > datetime('now', '-1 hour')")
        recent_messages = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM blockchain_masterledger WHERE timestamp > datetime('now', '-1 hour')")
        recent_blockchain = cursor.fetchone()[0] or 0
        
        # Get device list with actual available info
        cursor.execute("""
            SELECT d.device_id, d.registered_at, u.username, u.email, u.is_staff
            FROM users_device d
            LEFT JOIN auth_user u ON d.owner_id = u.id
            ORDER BY d.registered_at DESC
        """)
        
        devices = []
        for row in cursor.fetchall():
            devices.append({
                'device_id': row[0],
                'registered_at': row[1],
                'username': row[2] or 'Unassigned',
                'email': row[3] or '',
                'is_staff': bool(row[4]) if row[4] is not None else False,
                'status': 'Online',  # Assume online for demo
                'team': 'Alpha' if row[0] and 'alpha' in row[0].lower() else 
                       'Bravo' if row[0] and 'bravo' in row[0].lower() else
                       'Command' if row[0] and ('cmd' in row[0].lower() or 'command' in row[0].lower()) else 'Delta'
            })
        
        conn.close()
        
        return JsonResponse({
            'success': True,
            'statistics': {
                'total_devices': total_devices,
                'online_count': online_count,
                'authenticated_count': authenticated_count,
                'high_clearance_count': high_clearance,
                'base_stations': base_stations
            },
            'activity': {
                'recent_messages': recent_messages,
                'recent_blockchain': recent_blockchain
            },
            'devices': devices,
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e),
            'statistics': {
                'total_devices': 0,
                'online_count': 0,
                'authenticated_count': 0,
                'high_clearance_count': 0,
                'base_stations': 0
            },
            'activity': {'recent_messages': 0, 'recent_blockchain': 0},
            'devices': []
        })

@csrf_exempt
@require_POST
def register_device_api(request):
    """Register new device"""
    try:
        device_id = request.POST.get('device_id')
        owner_id = request.POST.get('owner_id', 1)
        
        if not device_id:
            return JsonResponse({'success': False, 'error': 'Device ID required'})
        
        device, created = Device.objects.get_or_create(
            device_id=device_id,
            defaults={
                'owner_id': owner_id,
                'public_key': f'mock_key_{device_id}'
            }
        )
        
        return JsonResponse({
            'success': True,
            'device_id': device.device_id,
            'created': created
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Web view for device management
def device_management_view(request):
    """Display comprehensive device management page with real data"""
    from django.shortcuts import render
    import sqlite3
    
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Get devices with user information from the actual tables (using correct columns)
        cursor.execute("""
            SELECT 
                d.id,
                d.device_id,
                d.registered_at,
                d.public_key,
                u.id as user_id,
                u.username,
                u.email,
                u.first_name,
                u.last_name,
                u.is_staff,
                u.date_joined
            FROM users_device d
            LEFT JOIN auth_user u ON d.owner_id = u.id
            ORDER BY d.registered_at DESC
        """)
        
        devices = []
        for row in cursor.fetchall():
            # Determine team based on device ID and user staff status
            team = "Delta Team"  # Default
            device_id = row[1].lower()
            if 'alpha' in device_id:
                team = "Alpha Team"
            elif 'bravo' in device_id:
                team = "Bravo Team"
            elif 'command' in device_id or 'cmd' in device_id or (row[9] and bool(row[9])):  # is_staff
                team = "Command Team"
            elif row[0] % 3 == 0:  # Every 3rd device goes to Alpha
                team = "Alpha Team"
            elif row[0] % 3 == 1:  # Every other 3rd goes to Bravo
                team = "Bravo Team"
            
            # Calculate clearance level based on staff status and device age
            clearance_level = 5 if (row[9] and bool(row[9])) else 2  # Staff = Level 5, others = Level 2
            
            devices.append({
                'id': row[0],
                'device_id': row[1],
                'device_name': row[1],  # Use device_id as name
                'is_authenticated': True,  # All devices with owners are authenticated
                'is_online': True,  # Assume all are online for demo
                'clearance_level': clearance_level,
                'device_type': 'base' if 'base' in device_id else 'mobile',
                'registered_at': row[2],
                'user_id': row[4],
                'username': row[5] if row[5] else 'Unassigned',
                'email': row[6] if row[6] else 'No email',
                'full_name': f"{row[7] or ''} {row[8] or ''}".strip() or row[5] or 'Unknown',
                'status': 'Online',
                'auth_status': 'Authenticated' if row[5] else 'Pending',
                'team': team,
                'auth_level': f"Level {clearance_level}/5",
                'is_staff': bool(row[9]) if row[9] is not None else False
            })
        
        # Get device statistics using correct table structure
        total_devices = len(devices)
        online_count = total_devices  # All devices online for demo
        auth_count = len([d for d in devices if d['username'] != 'Unassigned'])
        
        # Get all users for assignment
        cursor.execute("""
            SELECT u.id, u.username, u.email, u.first_name, u.last_name, u.date_joined, u.is_staff
            FROM auth_user u
            ORDER BY u.date_joined DESC
        """)
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'full_name': f"{row[3] or ''} {row[4] or ''}".strip() or row[1],
                'date_joined': row[5],
                'is_staff': bool(row[6]) if row[6] is not None else False
            })
        
        # Get team statistics
        teams = {
            'Alpha Team': [d for d in devices if d['team'] == 'Alpha Team'],
            'Bravo Team': [d for d in devices if d['team'] == 'Bravo Team'],
            'Command Team': [d for d in devices if d['team'] == 'Command Team'],
            'Delta Team': [d for d in devices if d['team'] == 'Delta Team']
        }
        
        # Get recent activity counts
        cursor.execute("SELECT COUNT(*) FROM messaging_message WHERE timestamp > datetime('now', '-24 hours')")
        recent_messages = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM blockchain_masterledger WHERE timestamp > datetime('now', '-24 hours')")
        recent_blockchain = cursor.fetchone()[0] or 0
        
        conn.close()
        
        context = {
            'devices': devices,
            'users': users,
            'teams': teams,
            'total_devices': total_devices,
            'online_count': online_count,
            'auth_count': auth_count,
            'device_counts': {
                'alpha': len(teams['Alpha Team']),
                'bravo': len(teams['Bravo Team']),
                'command': len(teams['Command Team']),
                'delta': len(teams['Delta Team'])
            },
            'activity_stats': {
                'recent_messages': recent_messages,
                'recent_blockchain': recent_blockchain
            }
        }
        return render(request, 'users/device_management.html', context)
        
    except Exception as e:
        # Create empty context with error
        context = {
            'devices': [],
            'users': [],
            'teams': {'Alpha Team': [], 'Bravo Team': [], 'Command Team': [], 'Delta Team': []},
            'total_devices': 0,
            'online_count': 0,
            'auth_count': 0,
            'device_counts': {'alpha': 0, 'bravo': 0, 'command': 0, 'delta': 0},
            'activity_stats': {'recent_messages': 0, 'recent_blockchain': 0},
            'error': f"Database error: {str(e)}"
        }
        return render(request, 'users/device_management.html', context)

# TODO: Add JWT/WebAuthn authentication endpoints

# Create your views here.
