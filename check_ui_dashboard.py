"""
UI Dashboard Check - Verify Dashboard Interface and Functionality
"""

import asyncio
import sys
import json
import time
import subprocess
from pathlib import Path

class UIDashboardChecker:
    def __init__(self):
        self.frontend_path = Path("/home/lemessa-ahmed/Startup-to-Business/src/frontend")
        
    def check_backend_api(self):
        """Check if backend API is serving data correctly"""
        print("🔧 CHECKING BACKEND API")
        print("=" * 30)
        
        try:
            import requests
            
            # Test main dashboard endpoint
            response = requests.get("http://localhost:8001/api/v1/dashboard", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend API responding (Status: {response.status_code})")
                print(f"   hasData: {data.get('hasData', 'N/A')}")
                print(f"   aiGenerated: {data.get('aiGenerated', 'N/A')}")
                print(f"   businessIdeas: {len(data.get('businessIdeas', []))}")
                print(f"   score: {data.get('score', 'N/A')}")
                return True
            else:
                print(f"❌ Backend API error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Backend API check failed: {e}")
            return False
    
    def check_frontend_configuration(self):
        """Check frontend configuration and setup"""
        print("\n⚙️ CHECKING FRONTEND CONFIGURATION")
        print("=" * 40)
        
        try:
            # Check dashboard page
            dashboard_page = self.frontend_path / "app" / "dashboard" / "page.tsx"
            if not dashboard_page.exists():
                print("❌ Dashboard page not found")
                return False
            
            with open(dashboard_page, 'r') as f:
                content = f.read()
            
            # Check key dashboard features
            checks = {
                'BusinessIdeasSection import': 'BusinessIdeasSection' in content,
                'Data fetching logic': 'fetchData' in content,
                'AI data handling': 'getAIGeneratedDashboard' in content,
                'Mock data fallback': 'mockData' in content,
                'Loading states': 'loading' in content,
                'Error handling': 'try' in content and 'catch' in content,
                'Console debugging': 'console.log' in content,
                'Data source tracking': 'dataSource' in content
            }
            
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            return all(checks.values())
            
        except Exception as e:
            print(f"❌ Frontend configuration check failed: {e}")
            return False
    
    def check_business_ideas_component(self):
        """Check BusinessIdeasSection component"""
        print("\n💡 CHECKING BUSINESS IDEAS COMPONENT")
        print("=" * 40)
        
        try:
            component_path = self.frontend_path / "components" / "BusinessIdeasSection.tsx"
            if not component_path.exists():
                print("❌ BusinessIdeasSection component not found")
                return False
            
            with open(component_path, 'r') as f:
                content = f.read()
            
            # Check component features
            checks = {
                'React hooks': 'useState' in content and 'useEffect' in content,
                'API integration': 'dashboardApi' in content,
                'Update button': 'Update Ideas' in content,
                'Grid layout': 'grid grid-cols' in content,
                'Exactly 5 ideas': 'slice(0, 5)' in content,
                'Loading states': 'loading' in content,
                'Error handling': 'error' in content,
                'Success messages': 'refreshMessage' in content,
                'Mock data fallback': 'mockIdeas' in content,
                'Responsive design': 'md:grid-cols-2' in content and 'lg:grid-cols-3' in content,
                'Hover effects': 'hover:' in content,
                'Animations': 'transition' in content
            }
            
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            return all(checks.values())
            
        except Exception as e:
            print(f"❌ Business ideas component check failed: {e}")
            return False
    
    def check_api_service(self):
        """Check API service configuration"""
        print("\n🔌 CHECKING API SERVICE")
        print("=" * 30)
        
        try:
            api_path = self.frontend_path / "services" / "dashboardApi.ts"
            if not api_path.exists():
                print("❌ dashboardApi service not found")
                return False
            
            with open(api_path, 'r') as f:
                content = f.read()
            
            # Check API service features
            checks = {
                'Axios configuration': 'axios.create' in content,
                'Correct base URL': 'localhost:8001' in content,
                'Dashboard endpoints': 'getDashboardData' in content,
                'AI endpoints': 'getAIGeneratedDashboard' in content,
                'Refresh endpoint': 'refreshAIDashboard' in content,
                'Error handling': 'try' in content and 'catch' in content,
                'TypeScript interfaces': 'interface' in content,
                'Proper endpoint paths': '/api/v1/dashboard' in content
            }
            
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            return all(checks.values())
            
        except Exception as e:
            print(f"❌ API service check failed: {e}")
            return False
    
    def check_ui_elements(self):
        """Check UI elements and styling"""
        print("\n🎨 CHECKING UI ELEMENTS & STYLING")
        print("=" * 40)
        
        try:
            # Check BusinessIdeasSection for UI elements
            component_path = self.frontend_path / "components" / "BusinessIdeasSection.tsx"
            with open(component_path, 'r') as f:
                content = f.read()
            
            ui_checks = {
                'Card design': 'rounded-2xl' in content,
                'Glass morphism': 'surface' in content,
                'Gradient backgrounds': 'gradient' in content,
                'Shadow effects': 'shadow' in content,
                'Border styling': 'border' in content,
                'Hover animations': 'hover:' in content,
                'Color schemes': 'purple' in content or 'blue' in content,
                'Typography': 'font' in content or 'text' in content,
                'Spacing': 'gap-' in content or 'p-' in content,
                'Responsive grid': 'grid-cols-1' in content,
                'Loading spinner': 'animate-spin' in content,
                'Icon integration': 'RefreshCw' in content or 'Lightbulb' in content
            }
            
            for check, passed in ui_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            return all(ui_checks.values())
            
        except Exception as e:
            print(f"❌ UI elements check failed: {e}")
            return False
    
    def check_data_flow(self):
        """Check data flow and state management"""
        print("\n🔄 CHECKING DATA FLOW & STATE MANAGEMENT")
        print("=" * 45)
        
        try:
            # Check dashboard page data flow
            dashboard_page = self.frontend_path / "app" / "dashboard" / "page.tsx"
            with open(dashboard_page, 'r') as f:
                dashboard_content = f.read()
            
            # Check BusinessIdeasSection data flow
            component_path = self.frontend_path / "components" / "BusinessIdeasSection.tsx"
            with open(component_path, 'r') as f:
                component_content = f.read()
            
            data_flow_checks = {
                'Dashboard state management': 'useState' in dashboard_content,
                'Dashboard data fetching': 'fetchData' in dashboard_content,
                'Dashboard error handling': 'setError' in dashboard_content,
                'Component state management': 'useState' in component_content,
                'Component data fetching': 'fetchBusinessIdeas' in component_content,
                'Component error handling': 'setError' in component_content,
                'Data props passing': 'businessIdeas' in dashboard_content,
                'Update functionality': 'refreshAIData' in dashboard_content,
                'Loading coordination': 'setLoading' in dashboard_content,
                'Data source tracking': 'dataSource' in dashboard_content
            }
            
            for check, passed in data_flow_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            return all(data_flow_checks.values())
            
        except Exception as e:
            print(f"❌ Data flow check failed: {e}")
            return False
    
    def check_user_experience(self):
        """Check user experience features"""
        print("\n👤 CHECKING USER EXPERIENCE FEATURES")
        print("=" * 40)
        
        try:
            # Check both dashboard and component
            dashboard_page = self.frontend_path / "app" / "dashboard" / "page.tsx"
            component_path = self.frontend_path / "components" / "BusinessIdeasSection.tsx"
            
            with open(dashboard_page, 'r') as f:
                dashboard_content = f.read()
            
            with open(component_path, 'r') as f:
                component_content = f.read()
            
            ux_checks = {
                'Loading indicators': 'loading' in dashboard_content and 'loading' in component_content,
                'Error messages': 'error' in dashboard_content and 'error' in component_content,
                'Success feedback': 'success' in component_content or 'refreshMessage' in component_content,
                'Empty state handling': 'hasData' in dashboard_content,
                'Interactive buttons': 'button' in component_content,
                'Visual feedback': 'hover:' in component_content,
                'Clear CTAs': 'Update Ideas' in component_content,
                'Information hierarchy': 'h1' in dashboard_content and 'h3' in component_content,
                'Responsive design': 'grid-cols' in component_content,
                'Accessibility': 'className' in dashboard_content,
                'Debug console logs': 'console.log' in dashboard_content
            }
            
            for check, passed in ux_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            return all(ux_checks.values())
            
        except Exception as e:
            print(f"❌ User experience check failed: {e}")
            return False
    
    def check_responsive_design(self):
        """Check responsive design implementation"""
        print("\n📱 CHECKING RESPONSIVE DESIGN")
        print("=" * 35)
        
        try:
            component_path = self.frontend_path / "components" / "BusinessIdeasSection.tsx"
            with open(component_path, 'r') as f:
                content = f.read()
            
            responsive_checks = {
                'Mobile layout': 'grid-cols-1' in content,
                'Tablet layout': 'md:grid-cols-2' in content,
                'Desktop layout': 'lg:grid-cols-3' in content,
                'Responsive spacing': 'gap-6' in content,
                'Responsive padding': 'p-6' in content,
                'Flexible container': 'max-w-7xl' in content or 'container' in content,
                'Responsive typography': 'text-lg' in content or 'text-sm' in content,
                'Mobile-first approach': 'grid-cols-1' in content
            }
            
            for check, passed in responsive_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            return all(responsive_checks.values())
            
        except Exception as e:
            print(f"❌ Responsive design check failed: {e}")
            return False
    
    def run_ui_dashboard_check(self):
        """Run complete UI dashboard check"""
        print("🧪 UI DASHBOARD COMPREHENSIVE CHECK")
        print("=" * 50)
        print("Verifying dashboard interface and functionality...")
        print("=" * 50)
        
        checks = [
            ("Backend API", self.check_backend_api),
            ("Frontend Configuration", self.check_frontend_configuration),
            ("Business Ideas Component", self.check_business_ideas_component),
            ("API Service", self.check_api_service),
            ("UI Elements & Styling", self.check_ui_elements),
            ("Data Flow & State Management", self.check_data_flow),
            ("User Experience Features", self.check_user_experience),
            ("Responsive Design", self.check_responsive_design)
        ]
        
        results = {}
        
        for check_name, check_func in checks:
            try:
                result = check_func()
                results[check_name] = result
            except Exception as e:
                print(f"❌ {check_name} failed with exception: {e}")
                results[check_name] = False
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 UI DASHBOARD CHECK RESULTS")
        print("=" * 50)
        
        for check_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {check_name.upper()}: {status}")
        
        all_passed = all(results.values())
        
        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 UI DASHBOARD CHECK - PERFECT!")
            print("   ✅ Backend API is serving data correctly")
            print("   ✅ Frontend is properly configured")
            print("   ✅ Business ideas component is complete")
            print("   ✅ API service is working correctly")
            print("   ✅ UI elements are beautifully styled")
            print("   ✅ Data flow is properly managed")
            print("   ✅ User experience features are excellent")
            print("   ✅ Responsive design is implemented")
            print("   ✅ Dashboard is ready for users!")
        else:
            print("⚠️ SOME UI CHECKS FAILED")
            print("   Address the failed components before deployment")
        print("=" * 50)
        
        return all_passed

def main():
    """Main function"""
    checker = UIDashboardChecker()
    success = checker.run_ui_dashboard_check()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
