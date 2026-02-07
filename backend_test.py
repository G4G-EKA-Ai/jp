#!/usr/bin/env python3
"""
JAYTI Birthday Website - Backend API Testing
Comprehensive Django endpoint testing for all features
"""

import requests
import json
import sys
from datetime import datetime
import os

class JaytiBackendTester:
    def __init__(self, base_url="https://ca9e8b67-68a2-4af1-b870-7d635103caf8.preview.emergentagent.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.csrf_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        
        print(f"🧪 Starting Jayti Backend Tests")
        print(f"🌐 Testing URL: {self.base_url}")
        print("=" * 50)

    def run_test(self, name, method, endpoint, expected_status=200, data=None, follow_redirects=False):
        """Run a single test and track results"""
        url = f"{self.base_url}{endpoint}" if not endpoint.startswith('http') else endpoint
        
        self.tests_run += 1
        print(f"\n🔍 Test {self.tests_run}: {name}")
        print(f"   {method} {endpoint}")
        
        try:
            # Handle CSRF token for POST requests
            headers = {}
            if method == 'POST':
                if data is None:
                    data = {}
                if isinstance(data, dict) and self.csrf_token:
                    data['csrfmiddlewaretoken'] = self.csrf_token
                
                # Add CSRF header as well
                if self.csrf_token:
                    headers['X-CSRFToken'] = self.csrf_token
                    headers['Referer'] = self.base_url
            
            # Make request
            if method == 'GET':
                response = self.session.get(url, allow_redirects=follow_redirects)
            elif method == 'POST':
                response = self.session.post(url, data=data, headers=headers, allow_redirects=follow_redirects)
            
            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"   ✅ PASS - Status: {response.status_code}")
                
                # Extract CSRF token from login page
                if 'csrfmiddlewaretoken' in response.text:
                    import re
                    # Try multiple patterns for CSRF token
                    patterns = [
                        r'name="csrfmiddlewaretoken" value="([^"]*)"',
                        r'csrfmiddlewaretoken["\']?\s*:\s*["\']([^"\']*)["\']',
                        r'csrf_token["\']?\s*:\s*["\']([^"\']*)["\']'
                    ]
                    for pattern in patterns:
                        csrf_match = re.search(pattern, response.text)
                        if csrf_match:
                            self.csrf_token = csrf_match.group(1)
                            print(f"   🔑 CSRF token extracted: {self.csrf_token[:10]}...")
                            break
                
                return True, response
            else:
                print(f"   ❌ FAIL - Expected {expected_status}, got {response.status_code}")
                self.failed_tests.append({
                    'name': name,
                    'endpoint': endpoint,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'url': url
                })
                return False, response
                
        except Exception as e:
            print(f"   💥 ERROR - {str(e)}")
            self.failed_tests.append({
                'name': name,
                'endpoint': endpoint,
                'error': str(e),
                'url': url
            })
            return False, None

    def test_health_check(self):
        """Test health check endpoint"""
        success, response = self.run_test(
            "Health Check",
            "GET",
            "/health/"
        )
        
        if success and response:
            try:
                health_data = response.json()
                print(f"   📊 Status: {health_data.get('status', 'unknown')}")
                print(f"   🗃️ Database: {health_data.get('checks', {}).get('database', 'unknown')}")
                print(f"   📁 Static Files: {health_data.get('checks', {}).get('staticfiles', 'unknown')}")
                print(f"   ⭐ Astrology: {health_data.get('checks', {}).get('astrology', 'unknown')}")
            except:
                print(f"   ⚠️  Health check response not JSON")
        
        return success

    def test_login_page(self):
        """Test login page loads"""
        success, response = self.run_test(
            "Login Page Load",
            "GET",
            "/"
        )
        
        if success and response:
            content = response.text.lower()
            checks = [
                ('login form', 'name="username"' in content),
                ('password field', 'name="password"' in content),
                ('daily thought', 'daily-thought' in content or 'thought' in content),
                ('time display', 'current-time' in content or 'clock' in content),
            ]
            
            for check_name, check_result in checks:
                status = "✅" if check_result else "❌"
                print(f"   {status} {check_name}")
        
        return success

    def test_login_authentication(self):
        """Test login with credentials jayati/jayati2026"""
        print(f"\n🔐 Testing Authentication")
        
        # First get login page for CSRF
        self.run_test("Get Login Page for CSRF", "GET", "/")
        
        # Now attempt login
        login_data = {
            'username': 'jayati',
            'password': 'jayati2026'
        }
        
        success, response = self.run_test(
            "Login with Credentials",
            "POST",
            "/",
            expected_status=302,  # Expect redirect to dashboard
            data=login_data,
            follow_redirects=False
        )
        
        if success and response:
            if 'dashboard' in response.headers.get('location', '').lower():
                print("   🎯 Redirect to dashboard confirmed")
                return True
            else:
                print(f"   ⚠️  Unexpected redirect: {response.headers.get('location', 'None')}")
        
        return success

    def test_dashboard_access(self):
        """Test dashboard access after login"""
        success, response = self.run_test(
            "Dashboard Access",
            "GET",
            "/dashboard/"
        )
        
        if success and response:
            content = response.text.lower()
            checks = [
                ('welcome message', 'welcome' in content),
                ('goals section', 'karma' in content or 'goals' in content),
                ('astro section', 'dharma' in content or 'astro' in content),
                ('diary section', 'thoughts' in content or 'diary' in content),
                ('notes section', 'memory' in content or 'notes' in content),
                ('ai chat section', 'doubt' in content or 'ask jayti' in content),
            ]
            
            for check_name, check_result in checks:
                status = "✅" if check_result else "❌"
                print(f"   {status} {check_name}")
        
        return success

    def test_notes_functionality(self):
        """Test notes feature"""
        print(f"\n📝 Testing Notes Feature")
        
        # Test notes list page
        success1, _ = self.run_test("Notes List", "GET", "/notes/")
        
        # Test note creation page
        success2, _ = self.run_test("Note Create Page", "GET", "/notes/create/")
        
        return success1 and success2

    def test_diary_functionality(self):
        """Test diary feature"""
        print(f"\n📖 Testing Diary Feature")
        
        # Test diary overview
        success1, _ = self.run_test("Diary Overview", "GET", "/diary/")
        
        # Test diary write page
        success2, _ = self.run_test("Diary Write Page", "GET", "/diary/write/")
        
        # Test diary calendar
        success3, _ = self.run_test("Diary Calendar", "GET", "/diary/calendar/")
        
        return success1 and success2 and success3

    def test_goals_functionality(self):
        """Test goals feature"""
        print(f"\n🎯 Testing Goals Feature")
        
        # Test goals list
        success1, _ = self.run_test("Goals List", "GET", "/goals/")
        
        # Test goal creation page
        success2, _ = self.run_test("Goal Create Page", "GET", "/goals/create/")
        
        # Test goals board
        success3, _ = self.run_test("Goals Board", "GET", "/goals/board/")
        
        return success1 and success2 and success3

    def test_astro_functionality(self):
        """Test astrology feature"""
        print(f"\n⭐ Testing Astrology Feature")
        
        # Test astro dashboard
        success1, _ = self.run_test("Astro Dashboard", "GET", "/astro/")
        
        # Test birth chart
        success2, _ = self.run_test("Birth Chart", "GET", "/astro/chart/")
        
        # Test house details
        success3, _ = self.run_test("House Details", "GET", "/astro/houses/")
        
        # Test dasha periods
        success4, _ = self.run_test("Dasha Periods", "GET", "/astro/dasha/")
        
        # Test predictions
        success5, _ = self.run_test("Predictions", "GET", "/astro/predictions/")
        
        return success1 and success2 and success3 and success4 and success5

    def test_ai_chat_functionality(self):
        """Test AI chat feature"""
        print(f"\n🤖 Testing AI Chat Feature")
        
        # Test chat interface
        success1, _ = self.run_test("AI Chat Interface", "GET", "/ai-chat/")
        
        # Test chat history
        success2, _ = self.run_test("AI Chat History", "GET", "/ai-chat/history/")
        
        return success1 and success2

    def test_profile_functionality(self):
        """Test profile feature"""
        print(f"\n👤 Testing Profile Feature")
        
        # Test profile page
        success1, _ = self.run_test("Profile Page", "GET", "/profile/")
        
        # Test password change page
        success2, _ = self.run_test("Password Change Page", "GET", "/password-change/")
        
        return success1 and success2

    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Comprehensive Backend Test Suite")
        print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test order matters due to authentication
        test_results = []
        
        # Basic functionality
        test_results.append(self.test_health_check())
        test_results.append(self.test_login_page())
        
        # Authentication flow
        auth_success = self.test_login_authentication()
        test_results.append(auth_success)
        
        if auth_success:
            # Protected pages (require login)
            test_results.append(self.test_dashboard_access())
            test_results.append(self.test_notes_functionality())
            test_results.append(self.test_diary_functionality())
            test_results.append(self.test_goals_functionality())
            test_results.append(self.test_astro_functionality())
            test_results.append(self.test_ai_chat_functionality())
            test_results.append(self.test_profile_functionality())
        else:
            print("❌ Authentication failed - skipping protected endpoints")
        
        self.print_summary()
        return self.tests_passed == self.tests_run

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"📈 Total Tests: {self.tests_run}")
        print(f"🎯 Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.failed_tests:
            print(f"\n💥 FAILED TESTS:")
            for i, test in enumerate(self.failed_tests, 1):
                print(f"  {i}. {test['name']}")
                print(f"     Endpoint: {test['endpoint']}")
                if 'error' in test:
                    print(f"     Error: {test['error']}")
                else:
                    print(f"     Expected: {test['expected']}, Got: {test['actual']}")
                print(f"     URL: {test['url']}")
                print()

def main():
    """Main test execution"""
    tester = JaytiBackendTester()
    
    try:
        success = tester.run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())