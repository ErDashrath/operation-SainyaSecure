# 🛡️ Operation SainyaSecure - Complete API Endpoints Documentation

## 📋 Summary

All API endpoints have been properly implemented, routed, and organized with consistent namespacing. The system now provides comprehensive REST API coverage for all functionality.

## 🔗 API Structure

### Base URLs:
- **Web UI**: `http://127.0.0.1:8000/`
- **API v1**: `http://127.0.0.1:8000/api/v1/`
- **GraphQL**: `http://127.0.0.1:8000/graphql/`

---

## 📊 Dashboard Endpoints

### Web UI
- `GET /` - Landing page
- `GET /dashboard/` - Main dashboard

### API Endpoints
- `GET /api/v1/dashboard/summary/` - Complete system summary (Auth required)
- `GET /api/v1/dashboard/audit-replay/` - Timeline of events (Auth required)
- `GET /api/v1/dashboard/system-status/` - System status (Auth required)
- `GET /dashboard/api/stats/` - Simple stats API (No auth)

---

## 👥 User Management Endpoints

### Web UI
- `GET /users/devices/` - Device list page (Auth required)
- `GET /users/soldiers/` - Soldier profiles (Auth required)

### API Endpoints
- `GET /api/v1/users/devices/` - List all devices (Auth required)
- `POST /api/v1/users/devices/` - Create new device (Auth required)
- `GET /api/v1/users/devices/{id}/` - Device details (Auth required)
- `GET /api/v1/users/devices/status/` - Device status overview (Auth required)
- `GET /api/v1/users/devices/by-id/{device_id}/` - Get device by ID (Auth required)
- `GET /api/v1/users/soldiers/` - List soldier profiles (Auth required)
- `POST /api/v1/users/register/` - Register new user with device (Auth required)

### Simple APIs
- `GET /users/api/device-status/` - Device status (No auth)
- `POST /users/api/register-device/` - Register device (No auth)

---

## 💬 Messaging Endpoints

### Web UI
- `GET /messaging/` - Message list page (Auth required)
- `GET /messaging/{id}/` - Message details (Auth required)
- `GET /messaging/peer/{peer_id}/` - Messages by peer (Auth required)

### API Endpoints
- `GET /api/v1/messaging/` - List all messages (Auth required)
- `POST /api/v1/messaging/` - Create new message (Auth required)
- `GET /api/v1/messaging/{id}/` - Message details (Auth required)
- `POST /api/v1/messaging/send-p2p/` - Send P2P message (Auth required)

### Simple APIs
- `POST /messaging/api/send/` - Send message (No auth) - **Used by dashboard**
- `GET /messaging/api/list/` - List messages (No auth)
- `GET /messaging/api/stats/` - Message statistics (No auth)

---

## 🔗 Blockchain Endpoints

### Web UI
- `GET /blockchain/` - Transaction list page (Auth required)
- `GET /blockchain/transactions/{id}/` - Transaction details (Auth required)

### API Endpoints
- `GET /api/v1/blockchain/` - List blockchain transactions (Auth required)
- `POST /api/v1/blockchain/` - Create transaction (Auth required)
- `POST /api/v1/blockchain/validate/` - Validate block (Auth required)
- `GET /api/v1/blockchain/command-center/` - Command center status (Auth required)
- `POST /api/v1/blockchain/switch-mode/` - Switch operational mode (Auth required)
- `GET /api/v1/blockchain/stats/` - Blockchain statistics (Auth required)
- `GET /api/v1/blockchain/recent/` - Recent transactions (Auth required)

### Simple APIs
- `GET /blockchain/api/stats/` - Blockchain stats (No auth)
- `POST /blockchain/api/switch-mode/` - Switch mode (No auth)

---

## 📡 P2P Sync Endpoints

### Web UI
- `GET /p2p_sync/blocks/` - Local ledger blocks (Auth required)
- `GET /p2p_sync/status/` - P2P status page (Auth required)

### API Endpoints
- `GET /api/v1/p2p-sync/blocks/` - List local blocks (Auth required)
- `POST /api/v1/p2p-sync/blocks/` - Create local block (Auth required)
- `POST /api/v1/p2p-sync/sync-ledger/` - Sync with master ledger (Auth required)
- `GET /api/v1/p2p-sync/status/` - P2P status (Auth required)
- `POST /api/v1/p2p-sync/switch-offline/` - Switch to offline mode (Auth required)
- `POST /api/v1/p2p-sync/switch-online/` - Switch to online mode (Auth required)
- `POST /api/v1/p2p-sync/sync/` - Manual sync (Auth required)

### Simple APIs
- `GET /p2p_sync/api/status/` - P2P status (No auth) - **Used by dashboard**
- `POST /p2p_sync/api/toggle/` - Toggle P2P mode (No auth) - **Used by dashboard**

---

## 🤖 AI Anomaly Detection Endpoints

### Web UI
- `GET /ai_anomaly/alerts/` - Anomaly alerts list (Auth required)
- `GET /ai_anomaly/flagged/` - Flagged messages (Auth required)

### API Endpoints
- `GET /api/v1/ai-anomaly/alerts/` - List anomaly alerts (Auth required)
- `POST /api/v1/ai-anomaly/alerts/` - Create alert (Auth required)
- `GET /api/v1/ai-anomaly/alerts/{id}/` - Alert details (Auth required)
- `POST /api/v1/ai-anomaly/analyze/` - Analyze message (Auth required)
- `GET /api/v1/ai-anomaly/stats/` - Anomaly statistics (Auth required)
- `GET /api/v1/ai-anomaly/recent/` - Recent anomalies (Auth required)

### Simple APIs
- `GET /ai_anomaly/api/stats/` - Anomaly stats (No auth)
- `POST /ai_anomaly/api/analyze/` - Analyze message (No auth)

---

## 🔧 Technical Implementation

### URL Namespace Organization
```python
# Web UI endpoints (direct access)
path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard_web'))
path('users/', include(('users.urls', 'users'), namespace='users_web'))
path('messaging/', include(('messaging.urls', 'messaging'), namespace='messaging_web'))

# API v1 endpoints (versioned API)
path('api/v1/users/', include(('users.urls', 'users'), namespace='users_api'))
path('api/v1/messaging/', include(('messaging.urls', 'messaging'), namespace='messaging_api'))
```

### Authentication Strategy
- **DRF Endpoints**: Require authentication (session/token based)
- **Simple APIs**: No authentication (for easy frontend integration)
- **Dashboard Integration**: Uses simple APIs for AJAX calls

### Serializers Implemented
- ✅ **Message Serializers**: Full, Create, Summary variants
- ✅ **Blockchain Serializers**: Transaction + Legacy table serializers
- ✅ **User Serializers**: Device, Soldier Profile
- ✅ **P2P Serializers**: Local blocks, Status, Sync results
- ✅ **AI Serializers**: Anomaly alerts

### Response Formats
All endpoints return consistent JSON responses:
```json
{
  "status": "success|error",
  "data": {...},
  "message": "Optional message",
  "timestamp": "ISO format"
}
```

---

## ✅ Features Working

1. **Dashboard Integration**: All dashboard widgets connect to working APIs
2. **Message Sending**: Form submission creates real database entries
3. **P2P Mode Toggle**: Working offline/online mode switching
4. **System Statistics**: Real-time data from database
5. **Blockchain Logging**: Operational mode switching with history
6. **Device Management**: Registration and status tracking
7. **AI Anomaly Detection**: Message analysis and flagging

---

## 🚀 Ready for Demo

The API is now fully functional and supports:
- ✅ Web dashboard interactions
- ✅ Mobile app integration (future)
- ✅ External system integration
- ✅ Real-time status updates
- ✅ Complete CRUD operations
- ✅ Military communication workflows

All endpoints are properly tested with the existing demo data and ready for production use!