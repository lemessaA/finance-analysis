"""
Test the business ideas API endpoints
"""

import requests
import json

def test_business_ideas_api():
    """Test the business ideas API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Business Ideas API...")
    
    # Test main business ideas endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/dashboard/business-ideas", timeout=5)
        print(f"Business Ideas Endpoint Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Got {len(data.get('ideas', []))} ideas")
            if data.get('ideas'):
                print(f"First idea: {data['ideas'][0]['title']}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test refresh endpoint
    try:
        response = requests.post(f"{base_url}/api/v1/dashboard/business-ideas/refresh", timeout=5)
        print(f"Refresh Endpoint Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Refresh success! Got {len(data.get('ideas', []))} ideas")
        else:
            print(f"❌ Refresh error: {response.text}")
    except Exception as e:
        print(f"❌ Refresh connection error: {e}")

if __name__ == "__main__":
    test_business_ideas_api()
