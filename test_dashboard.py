"""
Simple test to verify dashboard API functionality
"""

import requests
import json

def test_dashboard_api():
    """Test the dashboard API endpoint."""
    try:
        print("🧪 Testing Dashboard API...")
        
        # Test the main dashboard endpoint
        response = requests.get("http://localhost:8000/api/v1/dashboard/dashboard", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard API Success!")
            print(f"Score: {data.get('score')}")
            print(f"Market Size: {data.get('marketAnalysis', {}).get('marketSize')}")
            print(f"Competitors: {len(data.get('competitors', []))}")
            return True
        else:
            print("❌ Dashboard API Error:")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Backend server may not be running")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout Error - Request took too long")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_health_endpoint():
    """Test health endpoint."""
    try:
        print("\n🏥 Testing Health Endpoint...")
        
        response = requests.get("http://localhost:8000/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check Success!")
            print(f"App: {data.get('name')}")
            print(f"Version: {data.get('version')}")
            print(f"Environment: {data.get('environment')}")
            return True
        else:
            print("❌ Health Check Failed")
            return False
            
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting API Tests...\n")
    
    health_ok = test_health_endpoint()
    dashboard_ok = test_dashboard_api()
    
    print(f"\n📊 Test Results:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Dashboard API: {'✅ PASS' if dashboard_ok else '❌ FAIL'}")
    
    if health_ok and dashboard_ok:
        print("\n🎉 All tests passed! The dashboard is working with real data!")
    else:
        print("\n⚠️  Some tests failed. Check the backend server status.")
