"""
OPERATION SainyaSecure - Blockchain Storage Architecture
==================================================

This document explains where and how blockchain ledger records are stored
in our hybrid secure military communication system.

STORAGE LAYERS:
==============

1. LOCAL DATABASE (SQLite/PostgreSQL)
   ├── blockchain_blockchaintransaction (Master Ledger)
   ├── p2p_sync_localledgerblock (Local Mini-Ledgers) 
   ├── messaging_message (Encrypted Messages)
   └── users_device (Device Registry)

2. WEB3 BLOCKCHAIN (Optional - Ethereum/Polygon)
   ├── Smart Contract: MilitaryComm.sol
   ├── On-chain: Critical command transactions
   └── IPFS: Large payload storage

3. P2P MESH NETWORK
   ├── Local peer storage (offline resilience)
   ├── Direct device-to-device sync
   └── Conflict resolution via vector clocks

DETAILED BREAKDOWN:
==================

1. MASTER BLOCKCHAIN LEDGER (blockchain_blockchaintransaction):
   - Location: Django database table
   - Purpose: Central authoritative record
   - Fields:
     * tx_hash: Unique transaction identifier
     * block_id: Block chain reference  
     * sender/receiver: Device identifiers
     * payload_hash: SHA256 of message content
     * timestamp: When transaction occurred
     * lamport_clock: Logical ordering
     * vector_clock: Distributed sync metadata
     * is_synced: Web3 blockchain sync status
     * signature: Digital signature for integrity

2. LOCAL MINI-LEDGERS (p2p_sync_localledgerblock):
   - Location: Django database table  
   - Purpose: Offline P2P resilience
   - Fields:
     * block_id: Local block identifier
     * prev_hash: Previous block hash (blockchain)
     * device: Which device owns this block
     * is_synced: Sync status to master
     * sync_attempts: Failed sync counter
     * vector_clock: Conflict resolution data

3. WEB3 INTEGRATION (blockchain/web3_utils.py):
   - Current: Demo/mock implementation
   - Production: Connects to Ethereum node
   - Smart contracts handle critical transactions
   - IPFS for large file storage

4. MESSAGE STORAGE (messaging_message):
   - Encrypted payload storage
   - Links to blockchain via tx_hash
   - Anomaly detection flags
   - Device sender/receiver references

CURRENT DEVELOPMENT STATUS:
==========================

✅ SQLite database storage (active)
✅ Master ledger implementation 
✅ Local mini-ledger for P2P
✅ Vector clock conflict resolution
⚠️  Web3 integration (mock/demo mode)
⚠️  Smart contract deployment (pending)
⚠️  IPFS integration (planned)

DEMO DATA LOCATION:
==================
- Database file: db.sqlite3 (root directory)
- Tables contain sample military communication data
- Viewable through Django admin or dashboard
- API endpoints serve blockchain data to frontend

PRODUCTION DEPLOYMENT:
=====================
1. PostgreSQL for production database
2. Ethereum/Polygon for immutable ledger
3. IPFS for distributed file storage
4. Redis for real-time P2P coordination
5. Kubernetes for container orchestration

ACCESS METHODS:
==============
1. Django Admin: /admin/ (database tables)
2. Dashboard UI: /dashboard/ (user interface)  
3. GraphQL API: /graphql/ (programmatic access)
4. REST API: /api/*/ (mobile/external clients)
5. Direct SQL: Django ORM or raw queries
"""

# This is a documentation file explaining the blockchain storage architecture
print("Blockchain storage architecture documented")