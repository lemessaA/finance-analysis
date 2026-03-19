"""
Test dashboard data fetching with the fixed API endpoints
"""

import requests
import json

def test_dashboard_api():
    """Test the dashboard API endpoints with correct paths"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Dashboard API with Fixed Endpoints...")
    
    # Test main dashboard endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/dashboard/dashboard", timeout=10)
        print(f"Dashboard API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dashboard API working!")
            print(f"   Has Data: {data.get('hasData', 'N/A')}")
            print(f"   Score: {data.get('score', 'N/A')}")
            
            if data.get('userValidation'):
                print(f"   User Idea: {data['userValidation'].get('idea', 'N/A')}")
                print(f"   Industry: {data['userValidation'].get('industry', 'N/A')}")
            else:
                print("   No user validation data found")
        else:
            print(f"❌ Dashboard API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Dashboard API Connection Error: {e}")
    
    # Test business ideas endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/dashboard/business-ideas", timeout=5)
        print(f"Business Ideas API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Business Ideas API working!")
            print(f"   Ideas Count: {len(data.get('ideas', []))}")
            if data.get('ideas'):
                print(f"   First Idea: {data['ideas'][0].get('title', 'N/A')}")
        else:
            print(f"❌ Business Ideas API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Business Ideas API Connection Error: {e}")
    
    # Test startup validation to ensure data exists
    try:
        response = requests.post(f"{base_url}/api/v1/startup/validate", 
                               json={
                                   "idea": "Test startup for dashboard",
                                   "industry": "Technology",
                                   "target_market": "Enterprise",
                                   "additional_context": "Testing dashboard data flow"
                               }, timeout=30)
        print(f"Validation API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Validation working! Score: {data.get('overall_score', 'N/A')}")
            
            # Now test dashboard again
            print("\n🔄 Testing dashboard after validation...")
            dashboard_response = requests.get(f"{base_url}/api/v1/dashboard/dashboard", timeout=10)
            if dashboard_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                print(f"   Has Data: {dashboard_data.get('hasData', 'N/A')}")
                print(f"   Score: {dashboard_data.get('score', 'N/A')}")
                if dashboard_data.get('userValidation'):
                    print(f"   User Idea: {dashboard_data['userValidation'].get('idea', 'N/A')}")
        else:
            print(f"❌ Validation Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Validation API Error: {e}")

if __name__ == "__main__":
    test_dashboard_api()
