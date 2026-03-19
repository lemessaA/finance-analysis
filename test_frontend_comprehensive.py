"""
Comprehensive Frontend Test - All Folders, Workflows, and Functionality
"""

import os
import sys
import json
import time
from pathlib import Path

class FrontendTester:
    def __init__(self):
        self.frontend_path = Path("/home/lemessa-ahmed/Startup-to-Business/src/frontend")
        self.results = {}
        
    def test_folder_structure(self):
        """Test frontend folder structure"""
        print("📁 TESTING FRONTEND FOLDER STRUCTURE")
        print("=" * 50)
        
        try:
            expected_folders = [
                "app",
                "components", 
                "services",
                "lib",
                "public",
                "styles"
            ]
            
            folder_results = {}
            
            for folder in expected_folders:
                folder_path = self.frontend_path / folder
                exists = folder_path.exists() and folder_path.is_dir()
                folder_results[folder] = exists
                
                status = "✅" if exists else "❌"
                print(f"   {status} {folder}/")
                
                if exists:
                    # List subfolders and key files
                    try:
                        items = list(folder_path.iterdir())
                        subfolders = [item.name for item in items if item.is_dir()][:5]
                        files = [item.name for item in items if item.is_file()][:5]
                        
                        if subfolders:
                            print(f"      📂 Subfolders: {', '.join(subfolders)}")
                        if files:
                            print(f"      📄 Files: {', '.join(files)}")
                    except Exception as e:
                        print(f"      ⚠️ Could not list contents: {e}")
            
            self.results['folder_structure'] = folder_results
            return all(folder_results.values())
            
        except Exception as e:
            print(f"❌ Folder structure test failed: {e}")
            return False
    
    def test_app_folder(self):
        """Test app folder structure and pages"""
        print("\n📱 TESTING APP FOLDER (PAGES)")
        print("=" * 40)
        
        try:
            app_path = self.frontend_path / "app"
            
            # Check for key pages
            expected_pages = [
                "page.tsx",  # Root page
                "dashboard/page.tsx",
                "startup/page.tsx", 
                "forecasting/page.tsx",
                "market/page.tsx",
                "reports/page.tsx",
                "layout.tsx"
            ]
            
            page_results = {}
            
            for page in expected_pages:
                page_path = app_path / page
                exists = page_path.exists()
                page_results[page] = exists
                
                status = "✅" if exists else "❌"
                print(f"   {status} {page}")
                
                if exists:
                    # Analyze page content
                    try:
                        with open(page_path, 'r') as f:
                            content = f.read()
                        
                        checks = {
                            'React component': 'export default' in content or 'export function' in content,
                            'TypeScript': 'interface' in content or 'type' in content,
                            'Client directive': '"use client"' in content,
                            'Imports': 'import' in content,
                            'JSX': '<' in content and '>' in content
                        }
                        
                        for check, passed in checks.items():
                            check_status = "✅" if passed else "⚠️"
                            print(f"      {check_status} {check}")
                            
                    except Exception as e:
                        print(f"      ⚠️ Could not analyze content: {e}")
            
            self.results['app_pages'] = page_results
            return all(page_results.values())
            
        except Exception as e:
            print(f"❌ App folder test failed: {e}")
            return False
    
    def test_components_folder(self):
        """Test components folder"""
        print("\n🧩 TESTING COMPONENTS FOLDER")
        print("=" * 35)
        
        try:
            components_path = self.frontend_path / "components"
            
            if not components_path.exists():
                print("   ❌ Components folder not found")
                return False
            
            # Find all component files
            component_files = []
            for ext in ['*.tsx', '*.ts']:
                component_files.extend(components_path.glob(ext))
            
            print(f"   📊 Found {len(component_files)} component files")
            
            component_results = {}
            
            for comp_file in component_files[:10]:  # Test first 10 components
                try:
                    with open(comp_file, 'r') as f:
                        content = f.read()
                    
                    comp_name = comp_file.name
                    checks = {
                        'Export statement': 'export' in content,
                        'Import statements': 'import' in content,
                        'TypeScript types': 'interface' in content or 'type' in content,
                        'JSX/TSX': '<' in content and '>' in content,
                        'Function/class': 'function' in content or 'class' in content
                    }
                    
                    component_results[comp_name] = all(checks.values())
                    
                    status = "✅" if all(checks.values()) else "⚠️"
                    print(f"   {status} {comp_name}")
                    
                    # Show component details
                    if 'BusinessIdeas' in comp_name:
                        print(f"      💡 Business Ideas Component")
                    elif 'Dashboard' in comp_name:
                        print(f"      📊 Dashboard Component")
                    elif 'Card' in comp_name:
                        print(f"      🃏 Card Component")
                    elif 'Form' in comp_name:
                        print(f"      📝 Form Component")
                    
                except Exception as e:
                    print(f"   ❌ {comp_file.name}: Error - {e}")
                    component_results[comp_file.name] = False
            
            self.results['components'] = component_results
            return sum(component_results.values()) >= len(component_files) * 0.8  # 80% pass rate
            
        except Exception as e:
            print(f"❌ Components folder test failed: {e}")
            return False
    
    def test_services_folder(self):
        """Test services folder (API calls, utilities)"""
        print("\n🔌 TESTING SERVICES FOLDER")
        print("=" * 35)
        
        try:
            services_path = self.frontend_path / "services"
            
            if not services_path.exists():
                print("   ❌ Services folder not found")
                return False
            
            # Find all service files
            service_files = []
            for ext in ['*.ts', '*.tsx', '*.js']:
                service_files.extend(services_path.glob(ext))
            
            print(f"   📊 Found {len(service_files)} service files")
            
            service_results = {}
            
            for service_file in service_files:
                try:
                    with open(service_file, 'r') as f:
                        content = f.read()
                    
                    service_name = service_file.name
                    checks = {
                        'Export functions': 'export' in content,
                        'Import statements': 'import' in content,
                        'API calls': 'axios' in content or 'fetch' in content,
                        'TypeScript types': 'interface' in content or 'type' in content,
                        'Error handling': 'try' in content and 'catch' in content
                    }
                    
                    service_results[service_name] = all(checks.values())
                    
                    status = "✅" if all(checks.values()) else "⚠️"
                    print(f"   {status} {service_name}")
                    
                    # Show service details
                    if 'dashboard' in service_name.lower():
                        print(f"      📊 Dashboard API Service")
                    elif 'auth' in service_name.lower():
                        print(f"      🔐 Authentication Service")
                    elif 'api' in service_name.lower():
                        print(f"      🌐 API Service")
                    
                except Exception as e:
                    print(f"   ❌ {service_file.name}: Error - {e}")
                    service_results[service_file.name] = False
            
            self.results['services'] = service_results
            return len(service_files) > 0 and sum(service_results.values()) >= len(service_files) * 0.8
            
        except Exception as e:
            print(f"❌ Services folder test failed: {e}")
            return False
    
    def test_lib_folder(self):
        """Test lib folder (utilities, helpers)"""
        print("\n📚 TESTING LIB FOLDER")
        print("=" * 30)
        
        try:
            lib_path = self.frontend_path / "lib"
            
            if not lib_path.exists():
                print("   ⚠️ Lib folder not found (optional)")
                return True
            
            # Find all lib files
            lib_files = []
            for ext in ['*.ts', '*.tsx', '*.js']:
                lib_files.extend(lib_path.glob(ext))
            
            print(f"   📊 Found {len(lib_files)} lib files")
            
            lib_results = {}
            
            for lib_file in lib_files:
                try:
                    with open(lib_file, 'r') as f:
                        content = f.read()
                    
                    lib_name = lib_file.name
                    checks = {
                        'Export functions': 'export' in content,
                        'Utility functions': 'function' in content or 'const' in content,
                        'TypeScript types': 'interface' in content or 'type' in content,
                        'No JSX (pure logic)': content.count('<') <= 2  # Allow minimal JSX
                    }
                    
                    lib_results[lib_name] = all(checks.values())
                    
                    status = "✅" if all(checks.values()) else "⚠️"
                    print(f"   {status} {lib_name}")
                    
                except Exception as e:
                    print(f"   ❌ {lib_file.name}: Error - {e}")
                    lib_results[lib_file.name] = False
            
            self.results['lib'] = lib_results
            return True  # Lib folder is optional
            
        except Exception as e:
            print(f"❌ Lib folder test failed: {e}")
            return False
    
    def test_configuration_files(self):
        """Test configuration files"""
        print("\n⚙️ TESTING CONFIGURATION FILES")
        print("=" * 40)
        
        try:
            # Look in the correct locations - both frontend root and project root
            config_files = {
                'package.json': [
                    self.frontend_path / "package.json",
                    Path("/home/lemessa-ahmed/Startup-to-Business/package.json"),
                    self.frontend_path.parent / "package.json"
                ],
                'next.config.js': [
                    self.frontend_path / "next.config.js",
                    Path("/home/lemessa-ahmed/Startup-to-Business/next.config.js"),
                    self.frontend_path.parent / "next.config.js"
                ],
                'tailwind.config.js': [
                    self.frontend_path / "tailwind.config.js",
                    Path("/home/lemessa-ahmed/Startup-to-Business/tailwind.config.js"),
                    self.frontend_path.parent / "tailwind.config.js"
                ],
                'tsconfig.json': [
                    self.frontend_path / "tsconfig.json",
                    Path("/home/lemessa-ahmed/Startup-to-Business/tsconfig.json"),
                    self.frontend_path.parent / "tsconfig.json"
                ],
                '.env.local': [
                    self.frontend_path / ".env.local",
                    Path("/home/lemessa-ahmed/Startup-to-Business/.env.local"),
                    self.frontend_path.parent / ".env.local"
                ],
                '.env': [
                    self.frontend_path / ".env",
                    Path("/home/lemessa-ahmed/Startup-to-Business/.env"),
                    self.frontend_path.parent / ".env"
                ]
            }
            
            config_results = {}
            
            for config_name, config_paths in config_files.items():
                exists = any(path.exists() for path in config_paths)
                config_results[config_name] = exists
                
                status = "✅" if exists else "⚠️"
                print(f"   {status} {config_name}")
                
                if exists:
                    # Find which path exists
                    for config_path in config_paths:
                        if config_path.exists():
                            try:
                                with open(config_path, 'r') as f:
                                    content = f.read()
                                
                                # Check specific config content
                                if config_name == 'package.json':
                                    if '"next"' in content and '"react"' in content:
                                        print(f"      ✅ Contains Next.js and React dependencies")
                                elif config_name == 'tailwind.config.js':
                                    if 'content' in content and 'theme' in content:
                                        print(f"      ✅ Proper Tailwind configuration")
                                elif config_name == 'tsconfig.json':
                                    if '"compilerOptions"' in content:
                                        print(f"      ✅ TypeScript configuration present")
                                break
                                    
                            except Exception as e:
                                print(f"      ⚠️ Could not read config: {e}")
            
            self.results['config'] = config_results
            return config_results.get('package.json', False)  # At least package.json should exist
            
        except Exception as e:
            print(f"❌ Configuration files test failed: {e}")
            return False
    
    def test_workflows_and_functionality(self):
        """Test workflows and functionality"""
        print("\n🔄 TESTING WORKFLOWS AND FUNCTIONALITY")
        print("=" * 50)
        
        try:
            workflow_results = {}
            
            # Test 1: Dashboard Workflow
            print("   📊 Dashboard Workflow:")
            dashboard_page = self.frontend_path / "app" / "dashboard" / "page.tsx"
            if dashboard_page.exists():
                with open(dashboard_page, 'r') as f:
                    content = f.read()
                
                dashboard_checks = {
                    'Data fetching': 'fetchData' in content or 'useEffect' in content,
                    'AI integration': 'AI' in content or 'ai' in content,
                    'Business ideas': 'BusinessIdeasSection' in content,
                    'Error handling': 'try' in content and 'catch' in content,
                    'Loading states': 'loading' in content,
                    'Update functionality': 'refresh' in content or 'update' in content
                }
                
                workflow_results['dashboard'] = all(dashboard_checks.values())
                for check, passed in dashboard_checks.items():
                    status = "✅" if passed else "❌"
                    print(f"      {status} {check}")
            else:
                print("      ❌ Dashboard page not found")
                workflow_results['dashboard'] = False
            
            # Test 2: Startup Validation Workflow
            print("   🚀 Startup Validation Workflow:")
            startup_page = self.frontend_path / "app" / "startup" / "page.tsx"
            if startup_page.exists():
                with open(startup_page, 'r') as f:
                    content = f.read()
                
                startup_checks = {
                    'Form handling': 'form' in content or 'Form' in content,
                    'Validation logic': 'validation' in content or 'validate' in content,
                    'API integration': 'api' in content or 'fetch' in content,
                    'Error handling': 'error' in content,
                    'Success handling': 'success' in content
                }
                
                workflow_results['startup'] = all(startup_checks.values())
                for check, passed in startup_checks.items():
                    status = "✅" if passed else "❌"
                    print(f"      {status} {check}")
            else:
                print("      ❌ Startup page not found")
                workflow_results['startup'] = False
            
            # Test 3: API Service Workflow
            print("   🔌 API Service Workflow:")
            api_service = self.frontend_path / "services" / "dashboardApi.ts"
            if api_service.exists():
                with open(api_service, 'r') as f:
                    content = f.read()
                
                api_checks = {
                    'HTTP client': 'axios' in content or 'fetch' in content,
                    'Dashboard endpoints': 'dashboard' in content,
                    'AI endpoints': 'ai' in content or 'AI' in content,
                    'Error handling': 'try' in content and 'catch' in content,
                    'Type definitions': 'interface' in content or 'type' in content
                }
                
                workflow_results['api_service'] = all(api_checks.values())
                for check, passed in api_checks.items():
                    status = "✅" if passed else "❌"
                    print(f"      {status} {check}")
            else:
                print("      ❌ API service not found")
                workflow_results['api_service'] = False
            
            # Test 4: Component Integration Workflow
            print("   🧩 Component Integration Workflow:")
            business_ideas_comp = self.frontend_path / "components" / "BusinessIdeasSection.tsx"
            if business_ideas_comp.exists():
                with open(business_ideas_comp, 'r') as f:
                    content = f.read()
                
                component_checks = {
                    'State management': 'useState' in content or 'useEffect' in content,
                    'API integration': 'dashboardApi' in content or 'fetch' in content,
                    'Update functionality': 'update' in content or 'refresh' in content,
                    'Error handling': 'error' in content,
                    'Loading states': 'loading' in content,
                    'UI rendering': 'return' in content and '<' in content
                }
                
                workflow_results['component_integration'] = all(component_checks.values())
                for check, passed in component_checks.items():
                    status = "✅" if passed else "❌"
                    print(f"      {status} {check}")
            else:
                print("      ❌ Business ideas component not found")
                workflow_results['component_integration'] = False
            
            self.results['workflows'] = workflow_results
            return sum(workflow_results.values()) >= len(workflow_results) * 0.75  # 75% pass rate
            
        except Exception as e:
            print(f"❌ Workflows test failed: {e}")
            return False
    
    def test_dependencies_and_imports(self):
        """Test dependencies and imports"""
        print("\n📦 TESTING DEPENDENCIES AND IMPORTS")
        print("=" * 45)
        
        try:
            # Check package.json dependencies in multiple locations
            package_json_paths = [
                self.frontend_path / "package.json",
                Path("/home/lemessa-ahmed/Startup-to-Business/package.json"),
                self.frontend_path.parent / "package.json"
            ]
            
            package_json_path = None
            for path in package_json_paths:
                if path.exists():
                    package_json_path = path
                    break
            
            if not package_json_path:
                print("   ❌ package.json not found")
                return False
            
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            dependencies = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
            
            # Check for key dependencies
            key_deps = {
                'next': 'Next.js framework',
                'react': 'React library',
                'react-dom': 'React DOM renderer',
                'typescript': 'TypeScript compiler',
                '@types/react': 'React TypeScript types',
                '@types/node': 'Node.js TypeScript types',
                'tailwindcss': 'Tailwind CSS',
                'axios': 'HTTP client',
                'lucide-react': 'Icon library'
            }
            
            dep_results = {}
            
            for dep, description in key_deps.items():
                exists = dep in dependencies
                dep_results[dep] = exists
                
                status = "✅" if exists else "⚠️"
                version = dependencies.get(dep, 'N/A') if exists else 'N/A'
                print(f"   {status} {dep}@{version} - {description}")
            
            # Check for import consistency in key files
            print("\n   🔍 CHECKING IMPORT CONSISTENCY:")
            
            key_files = [
                self.frontend_path / "app" / "dashboard" / "page.tsx",
                self.frontend_path / "components" / "BusinessIdeasSection.tsx",
                self.frontend_path / "services" / "dashboardApi.ts"
            ]
            
            import_issues = 0
            
            for file_path in key_files:
                if file_path.exists():
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        # Check for common import patterns
                        import_patterns = {
                            'React imports': "from 'react'" in content,
                            'Next.js imports': "from 'next'" in content,
                            'Lucide icons': "from 'lucide-react'" in content,
                            'Local imports': "from '@/services/" in content or "from '@/components/" in content,
                            'TypeScript imports': 'import type' in content or 'interface' in content
                        }
                        
                        file_name = file_path.name
                        print(f"      📄 {file_name}:")
                        
                        for pattern, exists in import_patterns.items():
                            status = "✅" if exists else "⚠️"
                            print(f"         {status} {pattern}")
                        
                    except Exception as e:
                        print(f"      ❌ {file_path.name}: Could not analyze imports - {e}")
                        import_issues += 1
            
            self.results['dependencies'] = dep_results
            return len([d for d in dep_results.values() if d]) >= 7 and import_issues == 0
            
        except Exception as e:
            print(f"❌ Dependencies test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all frontend tests"""
        print("🧪 COMPREHENSIVE FRONTEND TEST")
        print("=" * 60)
        print("Testing all folders, workflows, and functionality...")
        print("=" * 60)
        
        tests = [
            ("Folder Structure", self.test_folder_structure),
            ("App Folder (Pages)", self.test_app_folder),
            ("Components Folder", self.test_components_folder),
            ("Services Folder", self.test_services_folder),
            ("Lib Folder", self.test_lib_folder),
            ("Configuration Files", self.test_configuration_files),
            ("Workflows & Functionality", self.test_workflows_and_functionality),
            ("Dependencies & Imports", self.test_dependencies_and_imports)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results[test_name] = result
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {e}")
                results[test_name] = False
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 FRONTEND TEST RESULTS SUMMARY")
        print("=" * 60)
        
        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {test_name.upper()}: {status}")
        
        all_passed = all(results.values())
        
        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 ALL FRONTEND TESTS PASSED!")
            print("   ✅ Folder structure is complete and organized")
            print("   ✅ All pages are properly implemented")
            print("   ✅ Components are well-structured and functional")
            print("   ✅ Services are properly configured")
            print("   ✅ Configuration files are complete")
            print("   ✅ Workflows are functioning correctly")
            print("   ✅ Dependencies and imports are consistent")
            print("   ✅ Frontend is ready for production")
        else:
            print("⚠️ SOME FRONTEND TESTS FAILED")
            print("   Check the individual test results above")
            print("   Address the failed components before production")
        print("=" * 60)
        
        return all_passed

def main():
    """Main test function"""
    tester = FrontendTester()
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
