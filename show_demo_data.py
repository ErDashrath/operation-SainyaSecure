import sqlite3
import json
from datetime import datetime

def show_existing_data():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    print("=== EXISTING DEMO DATA ===\n")
    
    # Users
    cursor.execute("SELECT id, username, email, first_name, last_name, is_superuser FROM auth_user")
    users = cursor.fetchall()
    print("USERS:")
    for user in users:
        print(f"  {user[0]}: {user[1]} ({user[2]}) - {user[3]} {user[4]} {'[ADMIN]' if user[5] else ''}")
    
    # Devices
    cursor.execute("SELECT id, device_id, owner_id, registered_at FROM users_device")
    devices = cursor.fetchall()
    print(f"\nDEVICES ({len(devices)} devices):")
    for device in devices:
        print(f"  {device[0]}: {device[1]} (Owner: {device[2]}) - {device[3]}")
    
    # Messages
    cursor.execute("SELECT id, msg_id, sender_id, receiver_id, timestamp, anomaly_flag FROM messaging_message")
    messages = cursor.fetchall()
    print(f"\nMESSAGES ({len(messages)} messages):")
    for msg in messages:
        print(f"  {msg[0]}: {msg[1]} (From: {msg[2]} To: {msg[3]}) - {msg[4]} {'⚠️ ANOMALY' if msg[5] else '✅'}")
    
    # Blockchain transactions
    cursor.execute("SELECT id, tx_hash, sender, receiver, timestamp, is_synced FROM blockchain_blockchaintransaction")
    transactions = cursor.fetchall()
    print(f"\nBLOCKCHAIN TRANSACTIONS ({len(transactions)} transactions):")
    for tx in transactions:
        print(f"  {tx[0]}: {tx[1][:16]}... (From: {tx[2]} To: {tx[3]}) - {tx[4]} {'✅ SYNCED' if tx[5] else '⏳ PENDING'}")
    
    # Master ledger (old blockchain implementation)
    cursor.execute("SELECT tx_hash, from_device_id, to_device_id, timestamp, mode_when_created FROM blockchain_masterledger")
    master_entries = cursor.fetchall()
    print(f"\nMASTER LEDGER ({len(master_entries)} entries):")
    for entry in master_entries:
        print(f"  {entry[0][:16]}... (From: {entry[1]} To: {entry[2]}) - {entry[3]} [{entry[4]} mode]")
    
    # Command center status
    cursor.execute("SELECT name, current_mode, is_active, global_lamport_clock FROM blockchain_commandcenter")
    cc = cursor.fetchall()
    print(f"\nCOMMAND CENTER:")
    for center in cc:
        print(f"  {center[0]}: {center[1].upper()} mode, {'ACTIVE' if center[2] else 'INACTIVE'}, Clock: {center[3]}")
    
    # Device status
    cursor.execute("SELECT device_id, device_type, is_authorized, is_online, clearance_level FROM blockchain_device")
    device_status = cursor.fetchall()
    print(f"\nDEVICE STATUS ({len(device_status)} devices):")
    for device in device_status:
        print(f"  {device[0]}: {device[1]} {'✅ AUTH' if device[2] else '❌ UNAUTH'} {'🟢 ONLINE' if device[3] else '🔴 OFFLINE'} (Level {device[4]})")
    
    # Mode changes
    cursor.execute("SELECT old_mode, new_mode, changed_by, timestamp, reason FROM blockchain_modechangelog ORDER BY timestamp DESC LIMIT 5")
    mode_changes = cursor.fetchall()
    print(f"\nRECENT MODE CHANGES ({len(mode_changes)} shown):")
    for change in mode_changes:
        print(f"  {change[3]}: {change[0]} → {change[1]} by {change[2]} ({change[4]})")
    
    conn.close()

if __name__ == "__main__":
    show_existing_data()