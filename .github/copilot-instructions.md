# Copilot Instructions for Hybrid Secure Military Communication System

This project is a modular Django + Next.js (React) application for secure, offline-first military messaging, blockchain logging, AI anomaly detection, and real-time P2P communication. Follow the checklist below for setup and development best practices.

## Checklist
- [ ] Clarify Project Requirements
- [ ] Scaffold the Project
- [ ] Customize the Project
- [ ] Install Required Extensions
- [ ] Compile the Project
- [ ] Create and Run Task
- [ ] Launch the Project
- [ ] Ensure Documentation is Complete

## Execution Guidelines
- Use Django REST Framework, Graphene-Django, channels, django-cors-headers, pycryptodome, celery, redis, psycopg2-binary (SQLite for dev).
- Modular Django apps: users, messaging, p2p_sync, blockchain, ai_anomaly, dashboard.
- Next.js frontend: SSR, modular React components, offline-first P2P messaging (WebRTC), IndexedDB/localForage for offline storage.
- Use open-source libraries only.
- Use class-based views, reusable templates/layouts, standard routing with include().
- All sensitive data encrypted at rest and in transit.
- Async tasks for blockchain write and AI inference.
- Update this file as you complete each step.
