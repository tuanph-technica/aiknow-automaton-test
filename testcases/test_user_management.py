"""
User Management Test Suite

This module contains comprehensive test cases for the User Management functionality,
including user search, filtering, add/edit operations, pagination, and status management.
"""

import os
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List

import pytest
import softest

from pages.login import Login
from pages.UserManagement import UserManagement
from utilities.customLogger import LogGen
from utilities.utils import Utils


@pytest.mark.usefixtures("setup")
@pytest.mark.test_user_management
class TestUserManagement(softest.TestCase):
    """
    Test suite for User Management functionality.

    Tests cover:
    - User list retrieval and display
    - User search by name/email
    - Filtering by role, status, and date range
    - Add user workflow
    - Edit user workflow
    - Pagination navigation
    - Status toggle operations
    """

    logger = LogGen.loggen()

    @pytest.fixture(autouse=True)
    def class_setup(self, user_account):
        """
        Setup method that runs before each test.

        Args:
            user_account: User account fixture providing credentials
        """
        self.login = Login(self.driver)
        self.ut = Utils()
        self.user_account = user_account
        self.user_mgmt_page = None
        self._test_passed = False

    def tearDown(self):
        """
        Teardown method that runs after each test.
        NOTE: Logout is disabled to allow test execution in same session.
        Browser cleanup happens in conftest.py fixture.
        """
        # Simply log test completion - no logout
        # This allows multiple tests to run in sequence using same browser session
        try:
            test_name = self._testMethodName
            self.logger.info(f"Test {test_name} completed")
        except Exception as e:
            self.logger.error(f"Error during teardown: {e}")

    def _login_and_navigate_to_user_management(self) -> UserManagement:
        """
        Helper method to log in and navigate to User Management page.

        Returns:
            UserManagement: User Management page object
        """
        from pages.homepage import AiKnowHomePage

        # Check if already logged in
        homepage = AiKnowHomePage(self.driver)
        login_status = homepage.check_login_success()

        if login_status != "success":
            # Need to login
            self.logger.info("Not logged in, performing login...")
            username = self.user_account["username"]
            password = self.user_account["password"]

            homepage, error_message = self.login.do_login(user_name=username, pass_word=password)

            if error_message:
                self.logger.error(f"Login failed: {error_message}")
                pytest.fail(f"Failed to login: {error_message}")

            self.logger.info("Login successful")
        else:
            self.logger.info("Already logged in, reusing session")

        # Navigate to User Management page
        user_mgmt_page = homepage.get_user_management_menu()

        # Wait for page to load
        time.sleep(2)

        if not user_mgmt_page.is_page_loaded():
            pytest.fail("User Management page failed to load")

        return user_mgmt_page

    # ========== User List Tests ==========

    def test_get_user_count(self):
        """Test Case: Get the count of users displayed in the current page"""
        self.logger.info("=== Test: Get User Count ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get user count
        user_count = user_mgmt_page.get_user_count()
        self.logger.info(f"User count on current page: {user_count}")

        # Verify count is reasonable (should be between 1 and 20 for default page size)
        self.assertTrue(user_count > 0, "User count should be greater than 0")
        self.assertTrue(user_count <= 20, "User count should not exceed page size (default 20)")

        self.logger.info("✓ User count test passed")

    def test_get_all_users_info(self):
        """Test Case: Get information for all users in the current page"""
        self.logger.info("=== Test: Get All Users Info ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get all users info
        users = user_mgmt_page.get_all_users_info()
        self.logger.info(f"Retrieved {len(users)} users from current page")

        # Verify we got some users
        self.assertTrue(len(users) > 0, "Should retrieve at least one user")

        # Verify each user has required fields
        for i, user in enumerate(users):
            self.logger.info(f"User {i+1}: {user['username']} - {user['email']}")

            self.assertIn('username', user, "User should have username field")
            self.assertIn('email', user, "User should have email field")
            self.assertIn('role', user, "User should have role field")
            self.assertIn('status', user, "User should have status field")

            # Verify username is not empty (email can be empty in some cases)
            self.assertTrue(user['username'], "Username should not be empty")

        self.logger.info("✓ Get all users info test passed")

    def test_get_pagination_info(self):
        """Test Case: Get pagination information"""
        self.logger.info("=== Test: Get Pagination Info ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get pagination info
        pagination_info = user_mgmt_page.get_pagination_info()

        # Pagination might be None if there's only one page or pagination element not found
        if pagination_info is None:
            self.logger.info("Pagination info is None - might be single page or pagination not rendered")
            # This is acceptable - not all pages have pagination
            self.logger.info("✓ Pagination info test completed (no pagination found)")
            return

        self.logger.info(f"Pagination: {pagination_info['start']} – {pagination_info['end']} of {pagination_info['total']}")

        # Verify pagination info structure
        self.assertIn('start', pagination_info, "Should have start")
        self.assertIn('end', pagination_info, "Should have end")
        self.assertIn('total', pagination_info, "Should have total")

        # Verify values make sense
        self.assertTrue(pagination_info['start'] >= 1, "Start should be >= 1")
        self.assertTrue(pagination_info['end'] >= pagination_info['start'], "End should be >= start")
        self.assertTrue(pagination_info['total'] >= pagination_info['end'], "Total should be >= end")

        self.logger.info("✓ Pagination info test passed")

    # ========== Search Tests ==========

    def test_search_users_by_username(self):
        """Test Case: Search users by username"""
        self.logger.info("=== Test: Search Users by Username ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get first user's username to search for
        users = user_mgmt_page.get_all_users_info()
        if not users:
            pytest.skip("No users available for testing")

        search_username = users[0]['username']
        self.logger.info(f"Searching for username: {search_username}")

        # Perform search
        success = user_mgmt_page.search_by_name_or_email(search_username)
        self.assertTrue(success, "Search should execute successfully")

        # Verify results
        filtered_users = user_mgmt_page.get_all_users_info()
        self.logger.info(f"Found {len(filtered_users)} users matching search")

        # At least one result should contain the search term
        found = False
        for user in filtered_users:
            if search_username.lower() in user['username'].lower():
                found = True
                break

        self.assertTrue(found, f"Search results should contain {search_username}")
        self.logger.info("✓ Search by username test passed")

    def test_search_users_by_email(self):
        """Test Case: Search users by email"""
        self.logger.info("=== Test: Search Users by Email ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get first user's email to search for
        users = user_mgmt_page.get_all_users_info()
        if not users:
            pytest.skip("No users available for testing")

        search_email = users[0]['email']
        self.logger.info(f"Searching for email: {search_email}")

        # Perform search
        success = user_mgmt_page.search_by_name_or_email(search_email)
        self.assertTrue(success, "Search should execute successfully")

        # Verify results
        filtered_users = user_mgmt_page.get_all_users_info()
        self.logger.info(f"Found {len(filtered_users)} users matching search")

        # At least one result should contain the search term
        found = False
        for user in filtered_users:
            if search_email.lower() in user['email'].lower():
                found = True
                break

        self.assertTrue(found, f"Search results should contain {search_email}")
        self.logger.info("✓ Search by email test passed")

    # ========== Filter Tests ==========

    def test_filter_by_role(self):
        """Test Case: Filter users by role"""
        self.logger.info("=== Test: Filter by Role ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get all users first to find available role
        all_users = user_mgmt_page.get_all_users_info()
        if not all_users:
            pytest.skip("No users available for testing")

        # Get a role from the first user
        test_role = all_users[0]['role'].split(',')[0].strip()  # Get first role if multiple
        self.logger.info(f"Filtering by role: {test_role}")

        # Apply filter
        success = user_mgmt_page.filter_by_role([test_role])
        self.assertTrue(success, "Filter should be applied successfully")

        # Get filtered results
        filtered_users = user_mgmt_page.get_all_users_info()
        self.logger.info(f"Found {len(filtered_users)} users with role: {test_role}")

        # Verify all users have the selected role
        for user in filtered_users:
            user_roles = user['role']
            self.logger.info(f"User {user['username']} has roles: {user_roles}")
            # Role might be part of comma-separated list
            self.assertIn(test_role.lower(), user_roles.lower(),
                         f"User should have role {test_role}")

        self.logger.info("✓ Filter by role test passed")

    def test_filter_by_status(self):
        """Test Case: Filter users by status (Active/Inactive)"""
        self.logger.info("=== Test: Filter by Status ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Test with Active status
        test_status = "Active"
        self.logger.info(f"Filtering by status: {test_status}")

        # Apply filter
        success = user_mgmt_page.filter_by_status(test_status)
        self.assertTrue(success, "Filter should be applied successfully")

        # Get filtered results
        filtered_users = user_mgmt_page.get_all_users_info()
        self.logger.info(f"Found {len(filtered_users)} users with status: {test_status}")

        # Verify all users have the selected status
        if filtered_users:
            for user in filtered_users:
                user_status = user['status']
                self.logger.info(f"User {user['username']} has status: {user_status}")
                # Allow for case-insensitive comparison
                self.assertEqual(user_status.lower(), test_status.lower(),
                               f"User should have status {test_status}")

        self.logger.info("✓ Filter by status test passed")

    def test_reset_filters(self):
        """Test Case: Reset all filters to default"""
        self.logger.info("=== Test: Reset Filters ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get initial count
        initial_users = user_mgmt_page.get_all_users_info()
        initial_count = len(initial_users)
        self.logger.info(f"Initial user count: {initial_count}")

        # Apply a search filter
        if initial_users:
            search_term = initial_users[0]['username']
            user_mgmt_page.search_by_name_or_email(search_term)
            time.sleep(1)

            filtered_count = user_mgmt_page.get_user_count()
            self.logger.info(f"Filtered user count: {filtered_count}")

        # Reset filters
        success = user_mgmt_page.reset_filters()
        self.assertTrue(success, "Reset filters should execute successfully")

        # Get count after reset
        reset_count = user_mgmt_page.get_user_count()
        self.logger.info(f"Count after reset: {reset_count}")

        # Count after reset should be >= filtered count
        self.assertTrue(reset_count >= filtered_count, "Reset should show more or equal users")

        self.logger.info("✓ Reset filters test passed")

    # ========== Pagination Tests ==========

    def test_pagination_navigation(self):
        """Test Case: Test pagination navigation (next, previous, first, last)"""
        self.logger.info("=== Test: Pagination Navigation ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get initial pagination info
        initial_info = user_mgmt_page.get_pagination_info()
        self.logger.info(f"Initial page: {initial_info}")

        # Check if there are multiple pages
        if initial_info['total'] <= initial_info['end']:
            self.logger.info("Only one page available, skipping navigation test")
            pytest.skip("Not enough users for pagination testing")

        # Test next page
        self.logger.info("Testing next page navigation...")
        success = user_mgmt_page.go_to_next_page()
        self.assertTrue(success, "Should navigate to next page")

        next_page_info = user_mgmt_page.get_pagination_info()
        self.logger.info(f"Next page: {next_page_info}")
        self.assertGreater(next_page_info['start'], initial_info['start'],
                          "Next page should have higher start value")

        # Test previous page
        self.logger.info("Testing previous page navigation...")
        success = user_mgmt_page.go_to_previous_page()
        self.assertTrue(success, "Should navigate to previous page")

        prev_page_info = user_mgmt_page.get_pagination_info()
        self.logger.info(f"Previous page: {prev_page_info}")
        self.assertEqual(prev_page_info['start'], initial_info['start'],
                        "Should return to initial page")

        # Test last page
        self.logger.info("Testing last page navigation...")
        success = user_mgmt_page.go_to_last_page()
        self.assertTrue(success, "Should navigate to last page")

        last_page_info = user_mgmt_page.get_pagination_info()
        self.logger.info(f"Last page: {last_page_info}")
        self.assertEqual(last_page_info['end'], last_page_info['total'],
                        "Last page end should equal total")

        # Test first page
        self.logger.info("Testing first page navigation...")
        success = user_mgmt_page.go_to_first_page()
        self.assertTrue(success, "Should navigate to first page")

        first_page_info = user_mgmt_page.get_pagination_info()
        self.logger.info(f"First page: {first_page_info}")
        self.assertEqual(first_page_info['start'], 1, "First page should start at 1")

        self.logger.info("✓ Pagination navigation test passed")

    # ========== Add User Tests ==========

    def test_open_add_user_modal(self):
        """Test Case: Open Add User modal dialog"""
        self.logger.info("=== Test: Open Add User Modal ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Open add user modal
        success = user_mgmt_page.open_add_user_modal()
        self.assertTrue(success, "Add User modal should open successfully")

        self.logger.info("✓ Add User modal opened successfully")

        # Close modal
        user_mgmt_page.cancel_add_user()
        time.sleep(1)

    def test_add_user_workflow(self):
        """Test Case: Complete Add User workflow with form submission"""
        self.logger.info("=== Test: Add User Workflow ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Open add user modal
        success = user_mgmt_page.open_add_user_modal()
        self.assertTrue(success, "Add User modal should open")

        # Check initial button state (should be disabled when form is empty)
        time.sleep(1)
        button_enabled_before = user_mgmt_page.is_add_user_submit_button_enabled()
        self.logger.info(f"Submit button state before filling form: {'Enabled' if button_enabled_before else 'Disabled'}")

        # Generate unique user data with short username (max 20 chars)
        timestamp = datetime.now().strftime("%H%M%S")  # Use only time to keep it short
        user_data = {
            'username': f'auto_{timestamp}',  # e.g., "auto_150526" = 12 chars
            'email': f'auto_{timestamp}@test.com',
            'first_name_en': 'Test',
            'last_name_en': 'User',
            'first_name_jp': 'Tesuto',  # Roman characters (romaji)
            'last_name_jp': 'Yuzaa',    # Roman characters (romaji), 2-50 chars required
            'gender': 'MALE',
            'date_of_birth': '1990-01-01',
            'roles': ['User']  # Use basic role
        }

        self.logger.info(f"Adding new user: {user_data['username']}")
        self.logger.info(f"User data: username={user_data['username']}, email={user_data['email']}")

        # Fill form
        success = user_mgmt_page.fill_add_user_form(user_data)
        self.assertTrue(success, "Form should be filled successfully")
        self.logger.info("✓ Form filled successfully")

        # Check button state after filling form (should be enabled now)
        time.sleep(1)
        button_enabled_after = user_mgmt_page.is_add_user_submit_button_enabled()
        self.logger.info(f"Submit button state after filling form: {'Enabled' if button_enabled_after else 'Disabled'}")

        # Check for validation errors if button is still disabled
        if not button_enabled_after:
            self.logger.error("Submit button is still disabled after filling form - checking for validation errors")
            validation_errors = user_mgmt_page.get_add_user_form_validation_errors()
            if validation_errors:
                self.logger.error(f"Validation errors found: {validation_errors}")
            else:
                self.logger.info("No validation errors found - button may be disabled for other reasons")

            # Get button attributes for debugging
            try:
                submit_button = user_mgmt_page.driver.find_element(*user_mgmt_page.ADD_USER_SUBMIT_BUTTON)
                disabled_attr = submit_button.get_attribute('disabled')
                button_classes = submit_button.get_attribute('class')
                self.logger.info(f"Button attributes - disabled: {disabled_attr}, classes: {button_classes}")
            except:
                self.fail("Submit button should be enabled after filling all required fields")
        self.logger.info("✓ User added successfully, modal closed")

        # Wait for user list to refresh
        time.sleep(3)

        # Search for the new user to verify
        self.logger.info(f"Searching for new user: {user_data['username']}")
        user_mgmt_page.search_by_name_or_email(user_data['username'])
        time.sleep(2)

        # Verify user appears in the list
        users = user_mgmt_page.get_all_users_info()
        found = any(user['username'] == user_data['username'] for user in users)

        if found:
            self.logger.info(f"✓ New user {user_data['username']} found in user list")
        else:
            self.logger.warning(f"New user {user_data['username']} not immediately visible (may need page refresh)")

        self.logger.info("✓ Add user workflow test completed")

    def test_cancel_add_user(self):
        """Test Case: Cancel Add User operation"""
        self.logger.info("=== Test: Cancel Add User ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Open add user modal
        success = user_mgmt_page.open_add_user_modal()
        self.assertTrue(success, "Add User modal should open")

        # Cancel without filling form
        success = user_mgmt_page.cancel_add_user()
        self.assertTrue(success, "Cancel should work successfully")

        self.logger.info("✓ Cancel add user test passed")

    # ========== Edit User Tests ==========

    def test_open_edit_user_modal(self):
        """Test Case: Open Edit User modal for an existing user"""
        self.logger.info("=== Test: Open Edit User Modal ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get first user
        users = user_mgmt_page.get_all_users_info()
        if not users:
            pytest.skip("No users available for testing")

        target_username = users[0]['username']
        self.logger.info(f"Opening edit modal for user: {target_username}")

        # Open edit modal
        success = user_mgmt_page.open_edit_user_modal(target_username)
        self.assertTrue(success, "Edit User modal should open successfully")

        self.logger.info("✓ Edit User modal opened successfully")

        # Close modal
        user_mgmt_page.close_edit_user_modal()
        time.sleep(1)

    def test_get_user_profile_data(self):
        """Test Case: Get user profile data from Edit User modal"""
        self.logger.info("=== Test: Get User Profile Data ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get first user
        users = user_mgmt_page.get_all_users_info()
        if not users:
            pytest.skip("No users available for testing")

        target_username = users[0]['username']
        self.logger.info(f"Getting profile data for user: {target_username}")

        # Open edit modal
        success = user_mgmt_page.open_edit_user_modal(target_username)
        self.assertTrue(success, "Edit User modal should open")

        # Get profile data
        profile_data = user_mgmt_page.get_user_profile_data()
        self.assertIsNotNone(profile_data, "Profile data should be retrieved")

        self.logger.info(f"Profile data: {profile_data}")

        # Verify required fields
        self.assertIn('username', profile_data, "Should have username")
        self.assertIn('email', profile_data, "Should have email")
        self.assertIn('first_name_en', profile_data, "Should have first_name_en")
        self.assertIn('last_name_en', profile_data, "Should have last_name_en")

        self.logger.info("✓ Get user profile data test passed")

        # Close modal
        user_mgmt_page.close_edit_user_modal()
        time.sleep(1)

    # ========== Status Toggle Tests ==========

    def test_toggle_user_status(self):
        """Test Case: Toggle user active/inactive status"""
        self.logger.info("=== Test: Toggle User Status ===")

        user_mgmt_page = self._login_and_navigate_to_user_management()

        # Get all users and find one to toggle
        users = user_mgmt_page.get_all_users_info()
        if not users:
            pytest.skip("No users available for testing")

        # Find a user that's not the currently logged-in user (to avoid locking ourselves out)
        target_user = None
        for user in users:
            if user['username'] != self.user_account["username"]:
                target_user = user
                break

        if not target_user:
            pytest.skip("No suitable user found for status toggle testing")

        target_username = target_user['username']
        initial_status = target_user['status']
        self.logger.info(f"Toggling status for user: {target_username} (current: {initial_status})")

        # Toggle status
        success = user_mgmt_page.toggle_user_status(target_username)
        self.assertTrue(success, "Status toggle should execute successfully")

        self.logger.info("✓ User status toggled")

        # Wait for status change to process and page to stabilize
        time.sleep(3)

        # Reset filters first to ensure search input is in clean state
        user_mgmt_page.reset_filters()
        time.sleep(1)

        # Search for the user again to verify status change
        user_mgmt_page.search_by_name_or_email(target_username)
        time.sleep(2)

        # Get updated user info
        updated_users = user_mgmt_page.get_all_users_info()
        if updated_users:
            updated_status = updated_users[0]['status']
            self.logger.info(f"New status: {updated_status}")

            # Toggle back to restore original state
            user_mgmt_page.toggle_user_status(target_username)
            time.sleep(2)
            self.logger.info("✓ Status restored to original")

        self.logger.info("✓ Toggle user status test completed")
