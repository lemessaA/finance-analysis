"""
Test the functionality of each frontend page
"""

import requests
from bs4 import BeautifulSoup
import json

class PageFunctionalityTester:
    def __init__(self):
        self.base_url = "http://localhost:3000"
        self.results = []
    
    def test_page_content(self, path: str, expected_elements: list):
        """Test if page contains expected elements"""
        url = f"{self.base_url}{path}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return {"success": False, "error": f"HTTP {response.status_code}"}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            found_elements = []
            missing_elements = []
            
            for element in expected_elements:
                if element['type'] == 'text':
                    if element['content'].lower() in response.text.lower():
                        found_elements.append(element['content'])
                    else:
                        missing_elements.append(element['content'])
                elif element['type'] == 'tag':
                    tags = soup.find_all(element['tag'])
                    if tags:
                        found_elements.append(f"{len(tags)} {element['tag']} tags")
                    else:
                        missing_elements.append(f"{element['tag']} tags")
                elif element['type'] == 'class':
                    elements = soup.find_all(class_=element['class'])
                    if elements:
                        found_elements.append(f"{len(elements)} elements with class '{element['class']}'")
                    else:
                        missing_elements.append(f"class '{element['class']}'")
            
            return {
                "success": len(missing_elements) == 0,
                "found": found_elements,
                "missing": missing_elements
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_all_pages_functionality(self):
        """Test functionality of all pages"""
        print("🔍 Testing Frontend Page Functionality...\n")
        
        # Define test cases for each page
        test_cases = [
            {
                "path": "/",
                "name": "Home Page",
                "expected_elements": [
                    {"type": "text", "content": "AI Business Intelligence"},
                    {"type": "text", "content": "Get Started"},
                    {"type": "class", "class": "hero"},
                ]
            },
            {
                "path": "/dashboard",
                "name": "Dashboard Page",
                "expected_elements": [
                    {"type": "text", "content": "Dashboard"},
                    {"type": "text", "content": "Business Idea Templates"},
                    {"type": "class", "class": "glass"},
                ]
            },
            {
                "path": "/startup",
                "name": "Startup Validation Page",
                "expected_elements": [
                    {"type": "text", "content": "Startup Validation"},
                    {"type": "text", "content": "Submit"},
                    {"type": "tag", "tag": "form"},
                ]
            },
            {
                "path": "/reports",
                "name": "Financial Reports Page",
                "expected_elements": [
                    {"type": "text", "content": "Financial"},
                    {"type": "text", "content": "Upload"},
                    {"type": "tag", "tag": "input"},
                ]
            },
            {
                "path": "/forecasting",
                "name": "Forecasting Page",
                "expected_elements": [
                    {"type": "text", "content": "Forecast"},
                    {"type": "tag", "tag": "form"},
                ]
            },
            {
                "path": "/market",
                "name": "Market Intelligence Page",
                "expected_elements": [
                    {"type": "text", "content": "Market"},
                    {"type": "text", "content": "Search"},
                ]
            }
        ]
        
        for test_case in test_cases:
            print(f"🧪 Testing {test_case['name']} functionality...")
            result = self.test_page_content(test_case['path'], test_case['expected_elements'])
            
            if result['success']:
                print(f"   ✅ All expected elements found")
                print(f"   📋 Found: {', '.join(result['found'][:3])}")
            else:
                print(f"   ❌ Missing elements: {', '.join(result['missing'])}")
                if 'error' in result:
                    print(f"   🚨 Error: {result['error']}")
            
            print()
    
    def test_dashboard_business_ideas(self):
        """Test the business ideas section specifically"""
        print("💡 Testing Business Ideas Section...")
        
        try:
            response = requests.get("http://localhost:3000/dashboard", timeout=10)
            if response.status_code != 200:
                print("   ❌ Dashboard not accessible")
                return
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for business ideas related content
            business_ideas_indicators = [
                "Business Idea Templates",
                "AI Beauty Concierge",
                "Sustainable Beauty Box",
                "Refresh Ideas",
                "Lightbulb"
            ]
            
            found_indicators = []
            for indicator in business_ideas_indicators:
                if indicator.lower() in response.text.lower():
                    found_indicators.append(indicator)
            
            if len(found_indicators) >= 2:
                print(f"   ✅ Business Ideas section is working")
                print(f"   📋 Found indicators: {', '.join(found_indicators[:3])}")
            else:
                print(f"   ⚠️  Business Ideas section may not be fully loaded")
                print(f"   📋 Found: {found_indicators}")
            
        except Exception as e:
            print(f"   ❌ Error testing Business Ideas: {e}")
    
    def test_interactive_elements(self):
        """Test if interactive elements are present"""
        print("🎯 Testing Interactive Elements...")
        
        try:
            response = requests.get("http://localhost:3000/dashboard", timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for buttons, forms, inputs
            buttons = soup.find_all('button')
            inputs = soup.find_all('input')
            forms = soup.find_all('form')
            
            print(f"   📊 Found {len(buttons)} buttons")
            print(f"   📊 Found {len(inputs)} input fields")
            print(f"   📊 Found {len(forms)} forms")
            
            if len(buttons) > 0:
                print("   ✅ Interactive elements are present")
            else:
                print("   ⚠️  No buttons found")
            
        except Exception as e:
            print(f"   ❌ Error testing interactive elements: {e}")

def main():
    """Main test function"""
    tester = PageFunctionalityTester()
    
    # Test page functionality
    tester.test_all_pages_functionality()
    
    # Test business ideas specifically
    tester.test_dashboard_business_ideas()
    
    # Test interactive elements
    tester.test_interactive_elements()
    
    print("🎉 Frontend functionality testing complete!")

if __name__ == "__main__":
    main()
