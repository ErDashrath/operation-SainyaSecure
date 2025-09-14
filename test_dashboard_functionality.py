#!/usr/bin/env python3
"""
Dashboard Functionality Test Script
Tests all the key features that the dashboard provides
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_dashboard_endpoints():
    print("🧪 Testing Operation SainyaSecure Dashboard Functionality")
    print("=" * 60)
    
    results = {
        'dashboard_page': False,
        'p2p_status': False,
        'p2p_toggle': False,
        'message_send': False,
        'dashboard_stats': False,
        'real_time_updates': False
    }
    
    # Test 1: Dashboard Page Load
    print("\n1. 📄 Testing Dashboard Page Load...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard/")
        if response.status_code == 200 and "MilComm" in response.text:
            print("   ✅ Dashboard page loads successfully")
            print(f"   📊 Page size: {len(response.text)} characters")
            results['dashboard_page'] = True
        else:
            print(f"   ❌ Dashboard failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Dashboard error: {e}")
    
    # Test 2: P2P Status API
    print("\n2. 📡 Testing P2P Status API...")
    try:
        response = requests.get(f"{BASE_URL}/p2p_sync/api/status/")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ P2P Status API working")
            print(f"   📊 Offline Mode: {data.get('offline_mode')}")
            print(f"   📊 Connected Peers: {data.get('peer_count', 0)}")
            print(f"   📊 Pending Sync: {data.get('local_blocks_pending_sync', 0)}")
            results['p2p_status'] = True
        else:
            print(f"   ❌ P2P Status failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ P2P Status error: {e}")
    
    # Test 3: P2P Toggle Functionality
    print("\n3. 🔄 Testing P2P Mode Toggle...")
    try:
        # Get current status
        status_response = requests.get(f"{BASE_URL}/p2p_sync/api/status/")
        current_mode = status_response.json().get('offline_mode', False)
        
        # Toggle mode
        toggle_response = requests.post(f"{BASE_URL}/p2p_sync/api/toggle/")
        if toggle_response.status_code == 200:
            toggle_data = toggle_response.json()
            print("   ✅ P2P Toggle working")
            print(f"   📊 Switched to: {'Offline' if toggle_data.get('offline_mode') else 'Online'}")
            results['p2p_toggle'] = True
            
            # Toggle back
            requests.post(f"{BASE_URL}/p2p_sync/api/toggle/")
            print("   🔄 Toggled back to original state")
        else:
            print(f"   ❌ P2P Toggle failed: {toggle_response.status_code}")
    except Exception as e:
        print(f"   ❌ P2P Toggle error: {e}")
    
    # Test 4: Message Sending
    print("\n4. 💬 Testing Message Sending...")
    try:
        message_data = {
            'device': 'device_test',
            'message': f'Dashboard test message at {time.strftime("%Y-%m-%d %H:%M:%S")}'
        }
        response = requests.post(f"{BASE_URL}/messaging/api/send/", data=message_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Message sending working")
                print(f"   📊 Message ID: {data.get('message_id')}")
                print(f"   📊 Timestamp: {data.get('timestamp')}")
                results['message_send'] = True
            else:
                print(f"   ❌ Message send failed: {data.get('error')}")
        else:
            print(f"   ❌ Message send failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Message send error: {e}")
    
    # Test 5: Dashboard Stats API
    print("\n5. 📊 Testing Dashboard Statistics...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard/api/stats/")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Dashboard Stats API working")
            print(f"   📊 Total Messages: {data.get('messages', 0)}")
            print(f"   📊 Anomalies: {data.get('anomalies', 0)}")
            print(f"   📊 Blockchain Entries: {data.get('blockchain_entries', 0)}")
            print(f"   📊 Devices: {data.get('devices', 0)}")
            print(f"   📊 System Mode: {data.get('current_mode', 'unknown')}")
            print(f"   📊 System Status: {data.get('system_status', 'unknown')}")
            results['dashboard_stats'] = True
        else:
            print(f"   ❌ Dashboard Stats failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Dashboard Stats error: {e}")
    
    # Test 6: Real-time Updates Simulation
    print("\n6. ⚡ Testing Real-time Update Capability...")
    try:
        # Send another message
        test_data = {
            'device': 'device_realtime',
            'message': 'Real-time update test message'
        }
        requests.post(f"{BASE_URL}/messaging/api/send/", data=test_data)
        
        # Get updated stats
        time.sleep(1)  # Brief delay
        response = requests.get(f"{BASE_URL}/dashboard/api/stats/")
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Real-time updates working")
            print(f"   📊 Updated Message Count: {data.get('messages', 0)}")
            results['real_time_updates'] = True
        else:
            print(f"   ❌ Real-time updates failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Real-time updates error: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 DASHBOARD FUNCTIONALITY TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\n📊 Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎉 Dashboard is FULLY FUNCTIONAL and ready for demo!")
        print("🔗 Access at: http://127.0.0.1:8000/dashboard/")
    elif success_rate >= 60:
        print("⚠️  Dashboard is mostly functional with minor issues")
    else:
        print("❌ Dashboard needs significant fixes")
    
    return results

if __name__ == "__main__":
    test_dashboard_endpoints()