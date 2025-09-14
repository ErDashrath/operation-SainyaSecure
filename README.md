# 🛡️ Operation SainyaSecure

**Hybrid Secure Military Communication System with P2P Architecture**

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

Operation SainyaSecure is a modular Django + Next.js application designed for secure, offline-first military messaging with blockchain logging, AI anomaly detection, and real-time P2P communication capabilities.

## ✨ Key Features

- **🔄 P2P Communication System**: Real-time peer-to-peer communication with offline-first architecture
- **🔗 Blockchain Integration**: Secure transaction logging with conflict resolution
- **📊 Real-time Dashboard**: Comprehensive command center with live updates
- **🔐 Military-grade Security**: End-to-end encryption and secure authentication
- **📱 Responsive Interface**: Modern military-themed UI with DaisyUI

## 🏗️ System Architecture

### Core Modules
- **users**: Device management and authentication
- **messaging**: Secure message handling
- **p2p_sync**: Peer-to-peer synchronization
- **blockchain**: Transaction logging and verification
- **dashboard**: Command center interface

### P2P Capabilities
- Toggle between Server Online and P2P Offline modes
- Realistic peer discovery with signal strength simulation
- Blockchain-based message routing
- Offline message queuing and synchronization

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Django 5.2.6
- SQLite (development) / PostgreSQL (production)

### Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/operation-SainyaSecure.git
cd operation-SainyaSecure

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create demo data
python show_demo_data.py

# Start development server
python manage.py runserver
```

### Access Points
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **P2P Control Center**: http://127.0.0.1:8000/p2p_sync/dashboard/
- **API Documentation**: See `API_ENDPOINTS_COMPLETE.md`

## 🧪 Testing

### Run P2P System Tests
```bash
python test_p2p_system.py
```

### Run All Tests
```bash
python manage.py test
```

## 📊 API Endpoints

### P2P Communication
- `GET /p2p_sync/api/status/` - Real-time P2P status
- `POST /p2p_sync/api/toggle/` - Toggle operation modes
- `GET /p2p_sync/api/discover/` - Peer discovery
- `POST /p2p_sync/api/sync/` - Synchronization management
- `POST /p2p_sync/api/send-message/` - P2P messaging

### Dashboard & Analytics
- `GET /dashboard/api/stats/` - System statistics
- `GET /dashboard/api/activity/` - Activity monitoring
- `GET /users/api/device-status/` - Device status

## 🔧 Configuration

### Environment Variables
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### Security Settings
- CSRF protection enabled
- Secure headers configured
- Military-grade encryption ready

## 🎯 Use Cases

- **Military Communications**: Secure field communications
- **Emergency Response**: Disaster recovery communications
- **Corporate Security**: Enterprise secure messaging
- **Research**: P2P networking studies

## 🛠️ Development

### Project Structure
```
operation-SainyaSecure/
├── military_comm/          # Main Django project
├── users/                  # User and device management
├── messaging/              # Message handling
├── p2p_sync/              # P2P communication
├── blockchain/            # Blockchain integration
├── ai_anomaly/           # AI monitoring
├── dashboard/            # Command center
├── templates/            # HTML templates
└── static/              # Static assets
```

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📈 Performance

- **Real-time Updates**: 5-second refresh intervals
- **Peer Discovery**: Simulates 5+ concurrent connections
- **Database**: Optimized for P2P operations
- **Blockchain Sync**: Efficient conflict resolution

## 🔐 Security Features

- End-to-end message encryption
- Blockchain transaction verification
- Lamport clock synchronization
- Vector clock conflict resolution
- Military-grade security protocols

## 📚 Documentation

- [API Documentation](API_ENDPOINTS_COMPLETE.md)
- [Blockchain Architecture](BLOCKCHAIN_STORAGE_ARCHITECTURE.py)
- [Deployment Guide](GITHUB_DEPLOYMENT_GUIDE.md)

## 🎉 Demo

Run the interactive demo:
```bash
python quick_demo.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/operation-SainyaSecure/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/operation-SainyaSecure/discussions)

## 🙏 Acknowledgments

- Built with Django and modern web technologies
- Inspired by military communication requirements
- P2P architecture based on distributed systems research

---

**⚡ Operation SainyaSecure - Securing Communications, Enabling Operations** 🛡️