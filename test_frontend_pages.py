"""
Test all frontend pages to ensure they're working correctly
"""

import requests
import json
from typing import Dict, List

class FrontendTester:
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.results = []
    
    def test_page(self, path: str, description: str) -> Dict:
        """Test a single page"""
        url = f"{self.base_url}{path}"
        result = {
            "path": path,
            "description": description,
            "status_code": None,
            "response_time": None,
            "success": False,
            "error": None
        }
        
        try:
            response = requests.get(url, timeout=10)
            result["status_code"] = response.status_code
            result["response_time"] = response.elapsed.total_seconds()
            result["success"] = response.status_code == 200
            
            if not result["success"]:
                result["error"] = f"HTTP {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            result["error"] = "Connection refused - frontend server may not be running"
        except requests.exceptions.Timeout:
            result["error"] = "Request timeout"
        except Exception as e:
            result["error"] = str(e)
        
        self.results.append(result)
        return result
    
    def test_all_pages(self):
        """Test all known frontend pages"""
        print("🧪 Testing All Frontend Pages...\n")
        
        # Define all pages to test
        pages = [
            ("/", "Home Page"),
            ("/dashboard", "Dashboard Page"),
            ("/startup", "Startup Validation Page"),
            ("/reports", "Financial Reports Page"),
            ("/forecasting", "Forecasting Page"),
            ("/market", "Market Intelligence Page"),
        ]
        
        for path, description in pages:
            print(f"📍 Testing {description} ({path})...")
            result = self.test_page(path, description)
            
            if result["success"]:
                print(f"   ✅ {result['status_code']} - {result['response_time']:.2f}s")
            else:
                print(f"   ❌ {result['error']}")
        
        self.print_summary()
    
    def test_api_endpoints(self):
        """Test backend API endpoints that frontend pages depend on"""
        print("\n🔗 Testing Backend API Endpoints...\n")
        
        api_base = "http://localhost:8000/api/v1"
        endpoints = [
            ("/", "Health Check"),
            ("/dashboard/dashboard", "Dashboard Data"),
            ("/dashboard/business-ideas", "Business Ideas"),
            ("/startup/validate", "Startup Validation Endpoint"),
        ]
        
        for path, description in endpoints:
            print(f"🔌 Testing {description} ({path})...")
            url = f"{api_base}{path}"
            
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {response.status_code}")
                elif response.status_code == 405:  # Method not allowed for POST endpoints
                    print(f"   ✅ {response.status_code} (POST endpoint)")
                else:
                    print(f"   ❌ {response.status_code}")
            except Exception as e:
                print(f"   ❌ {e}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n📊 Test Summary:")
        print("=" * 50)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["success"])
        failed = total - passed
        
        print(f"Total Pages: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\n❌ Failed Pages:")
            for result in self.results:
                if not result["success"]:
                    print(f"   • {result['path']} - {result['error']}")
        
        print("\n" + "=" * 50)
        
        if failed == 0:
            print("🎉 All frontend pages are working correctly!")
        else:
            print("⚠️  Some pages have issues. Check the errors above.")

def main():
    """Main test function"""
    tester = FrontendTester()
    
    # Test frontend pages
    tester.test_all_pages()
    
    # Test backend API endpoints
    tester.test_api_endpoints()
    
    # Additional check for common issues
    print("\n🔍 Additional Checks:")
    
    # Check if frontend is running
    try:
        response = requests.get("http://localhost:3000", timeout=2)
        print("✅ Frontend server is running")
    except:
        print("❌ Frontend server is not running on port 3000")
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/", timeout=2)
        print("✅ Backend server is running")
    except:
        print("❌ Backend server is not running on port 8000")

if __name__ == "__main__":
    main()
