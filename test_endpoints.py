#!/usr/bin/env python3
"""
API Endpoint Testing Script for Operation TRINETRA
================================================

This script tests all the API endpoints to ensure they're working properly
with the demo data and can be used by frontend applications.
"""

import requests
import json
import sys
from urllib.parse import urljoin

class APITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def test_endpoint(self, method, endpoint, data=None, expected_status=200, auth_required=False):
        """Test a single API endpoint"""
        url = urljoin(self.base_url, endpoint)
        
        try:
            if method == 'GET':
                response = self.session.get(url)
            elif method == 'POST':
                response = self.session.post(url, data=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == expected_status
            
            result = {
                'endpoint': endpoint,
                'method': method,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'success': success,
                'response_size': len(response.content),
                'content_type': response.headers.get('content-type', 'unknown')
            }
            
            if not success:
                result['error'] = response.text[:200]
            
            self.test_results.append(result)
            return result
            
        except Exception as e:
            result = {
                'endpoint': endpoint,
                'method': method,
                'success': False,
                'error': str(e)
            }
            self.test_results.append(result)
            return result
    
    def run_comprehensive_tests(self):
        """Run tests on all major API endpoints"""
        print("🚀 Starting comprehensive API endpoint testing...")
        print("=" * 60)
        
        # Dashboard endpoints
        print("\n📊 Testing Dashboard Endpoints:")
        self.test_endpoint('GET', '/')
        self.test_endpoint('GET', '/dashboard/')
        self.test_endpoint('GET', '/api/v1/dashboard/summary/', expected_status=401)  # Auth required
        self.test_endpoint('GET', '/dashboard/api/stats/')
        
        # User endpoints
        print("\n👥 Testing User Endpoints:")
        self.test_endpoint('GET', '/api/v1/users/devices/', expected_status=401)  # Auth required
        self.test_endpoint('GET', '/users/api/device-status/')
        self.test_endpoint('POST', '/users/api/register-device/', data={'device_id': 'test_device_001'})
        
        # Messaging endpoints
        print("\n💬 Testing Messaging Endpoints:")
        self.test_endpoint('GET', '/api/v1/messaging/', expected_status=401)  # Auth required
        self.test_endpoint('GET', '/messaging/api/list/')
        self.test_endpoint('GET', '/messaging/api/stats/')
        self.test_endpoint('POST', '/messaging/api/send/', data={
            'device': 'device_001',
            'message': 'Test message from API tester'
        })
        
        # Blockchain endpoints
        print("\n🔗 Testing Blockchain Endpoints:")
        self.test_endpoint('GET', '/api/v1/blockchain/', expected_status=401)  # Auth required
        self.test_endpoint('GET', '/blockchain/api/stats/')
        self.test_endpoint('POST', '/blockchain/api/switch-mode/', data={
            'mode': 'normal',
            'reason': 'API test'
        })
        
        # P2P Sync endpoints
        print("\n📡 Testing P2P Sync Endpoints:")
        self.test_endpoint('GET', '/api/v1/p2p-sync/blocks/', expected_status=401)  # Auth required
        self.test_endpoint('GET', '/p2p_sync/api/status/')
        self.test_endpoint('POST', '/p2p_sync/api/toggle/')
        
        # AI Anomaly endpoints
        print("\n🤖 Testing AI Anomaly Endpoints:")
        self.test_endpoint('GET', '/api/v1/ai-anomaly/alerts/', expected_status=401)  # Auth required
        self.test_endpoint('GET', '/ai_anomaly/api/stats/')
        self.test_endpoint('POST', '/ai_anomaly/api/analyze/', data={'message_id': '1'})
        
        # GraphQL endpoint
        print("\n📊 Testing GraphQL Endpoint:")
        self.test_endpoint('GET', '/graphql/')
    
    def print_results(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📋 API ENDPOINT TEST RESULTS")
        print("=" * 60)
        
        passed = sum(1 for r in self.test_results if r['success'])
        failed = len(self.test_results) - passed
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Total: {len(self.test_results)}")
        print(f"📈 Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        
        # Show detailed results
        print(f"\n📝 Detailed Results:")
        for result in self.test_results:
            status_icon = "✅" if result['success'] else "❌"
            method = result.get('method', 'UNK')
            endpoint = result['endpoint']
            
            if result['success']:
                status_code = result.get('status_code', 'N/A')
                size = result.get('response_size', 0)
                print(f"  {status_icon} {method:4} {endpoint:40} [{status_code}] ({size} bytes)")
            else:
                error = result.get('error', 'Unknown error')[:50]
                print(f"  {status_icon} {method:4} {endpoint:40} ERROR: {error}")
        
        # Show recommendations
        if failed > 0:
            print(f"\n💡 Recommendations:")
            print(f"  - Check that Django server is running on {self.base_url}")
            print(f"  - Verify database migrations are applied")
            print(f"  - Check for authentication issues on protected endpoints")
            print(f"  - Review server logs for detailed error information")
    
    def test_specific_functionality(self):
        """Test specific functionality that the demo relies on"""
        print("\n🎯 Testing Demo-Specific Functionality:")
        
        # Test message sending
        print("\n📤 Testing Message Sending...")
        result = self.test_endpoint('POST', '/messaging/api/send/', data={
            'device': 'device_001',
            'message': 'Demo test message - this should appear in the dashboard'
        })
        
        if result['success']:
            print("  ✅ Message sending works - check dashboard for new message")
        
        # Test P2P mode toggle
        print("\n🔄 Testing P2P Mode Toggle...")
        result = self.test_endpoint('POST', '/p2p_sync/api/toggle/')
        
        if result['success']:
            print("  ✅ P2P mode toggle works")
        
        # Test system statistics
        print("\n📊 Testing System Statistics...")
        endpoints = [
            '/dashboard/api/stats/',
            '/messaging/api/stats/',
            '/blockchain/api/stats/',
            '/ai_anomaly/api/stats/'
        ]
        
        stats_working = 0
        for endpoint in endpoints:
            result = self.test_endpoint('GET', endpoint)
            if result['success']:
                stats_working += 1
        
        print(f"  📈 {stats_working}/{len(endpoints)} statistics endpoints working")

def main():
    print("🛡️ Operation TRINETRA - API Endpoint Validator")
    print("Testing all API endpoints for functionality and accessibility")
    
    tester = APITester()
    
    # Run comprehensive tests
    tester.run_comprehensive_tests()
    
    # Test demo-specific functionality
    tester.test_specific_functionality()
    
    # Print results
    tester.print_results()
    
    # Determine exit code
    failed_count = sum(1 for r in tester.test_results if not r['success'])
    if failed_count == 0:
        print(f"\n🎉 All endpoints are working! The API is ready for demo.")
        sys.exit(0)
    else:
        print(f"\n⚠️  Some endpoints have issues. Please review and fix before demo.")
        sys.exit(1)

if __name__ == "__main__":
    main()