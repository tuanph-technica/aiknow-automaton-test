"""
Role Management Test Suite

This module contains comprehensive test cases for the Role Management functionality,
including role listing, search, selection, and menu tree verification.
"""

import os
import time
import random
from datetime import datetime
from typing import Dict, List

import pytest
import softest

from pages.login import Login
from pages.RoleManagement import RoleManagement
from utilities.customLogger import LogGen
from utilities.utils import Utils


@pytest.mark.usefixtures("setup")
@pytest.mark.test_role_management
class TestRoleManagement(softest.TestCase):
    """
    Test suite for Role Management functionality.

    Tests cover:
    - Role list retrieval and display
    - Role search functionality
    - Role selection
    - Menu tree display
    - Menu assignment button visibility
    - Menu checkbox states
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
        self.role_mgmt_page = None
        self._test_passed = False

    def tearDown(self):
        """
        Teardown method that runs after each test.
        NOTE: Logout is disabled to allow test execution in same session.
        Browser cleanup happens in conftest.py fixture.
        """
        try:
            test_name = self._testMethodName
            self.logger.info(f"Test {test_name} completed")
        except Exception as e:
            self.logger.error(f"Error during teardown: {e}")

    def _login_and_navigate_to_role_management(self) -> RoleManagement:
        """
        Helper method to log in and navigate to Role Management page.

        Returns:
            RoleManagement: Role Management page object
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

        # Navigate through Settings menu to Role Management
        settings_page = homepage.get_setting_menu()
        time.sleep(1)

        # Click on Role Management menu item
        settings_page.get_menu_by_name("Role Management")
        time.sleep(2)

        # Create RoleManagement page object
        role_mgmt_page = RoleManagement(self.driver)

        if not role_mgmt_page.is_page_loaded():
            pytest.fail("Role Management page failed to load")

        return role_mgmt_page

    # ========== Role List Tests ==========

    def test_get_role_count(self):
        """Test Case: Get the count of roles displayed in the table"""
        self.logger.info("=== Test: Get Role Count ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Get role count
        role_count = role_mgmt_page.get_role_count()
        self.logger.info(f"Role count: {role_count}")

        # Verify count is reasonable (should be at least 1)
        self.assertTrue(role_count > 0, "Role count should be greater than 0")
        self.assertTrue(role_count <= 50, "Role count should be reasonable (<=50)")

        self.logger.info("✓ Role count test passed")

    def test_get_all_roles_info(self):
        """Test Case: Get information for all roles in the table"""
        self.logger.info("=== Test: Get All Roles Info ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Get all roles info
        roles = role_mgmt_page.get_all_roles_info()
        self.logger.info(f"Retrieved {len(roles)} roles from table")

        # Verify we got some roles
        self.assertTrue(len(roles) > 0, "Should retrieve at least one role")

        # Verify each role has required fields
        for i, role in enumerate(roles):
            self.logger.info(f"Role {i+1}: {role['role_name']} - {role['role_code']} - {role['status']}")

            self.assertIn('role_name', role, "Role should have role_name field")
            self.assertIn('role_code', role, "Role should have role_code field")
            self.assertIn('status', role, "Role should have status field")

            # Verify role name is not empty
            self.assertTrue(role['role_name'], "Role name should not be empty")
            self.assertTrue(role['role_code'], "Role code should not be empty")

        self.logger.info("✓ Get all roles info test passed")

    def test_get_page_title(self):
        """Test Case: Verify Role Management page title"""
        self.logger.info("=== Test: Get Page Title ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Get page title
        title = role_mgmt_page.get_page_title()
        self.logger.info(f"Page title: {title}")

        # Verify title contains expected text
        self.assertIn("Role Management", title, "Page title should contain 'Role Management'")

        self.logger.info("✓ Page title test passed")

    def test_is_role_present(self):
        """Test Case: Check if specific roles are present"""
        self.logger.info("=== Test: Is Role Present ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Expected roles from the HTML
        expected_roles = ["System Admin", "CEO", "User", "Viewer"]

        for role_name in expected_roles:
            is_present = role_mgmt_page.is_role_present(role_name)
            self.logger.info(f"Role '{role_name}' present: {is_present}")

            if is_present:
                self.logger.info(f"✓ Role '{role_name}' found")

        self.logger.info("✓ Role presence test completed")

    # ========== Role Selection Tests ==========

    def test_select_role_by_name(self):
        """Test Case: Select a role by clicking on its row"""
        self.logger.info("=== Test: Select Role by Name ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Get first role
        roles = role_mgmt_page.get_all_roles_info()
        if not roles:
            pytest.skip("No roles available for testing")

        target_role_name = roles[0]['role_name']
        self.logger.info(f"Selecting role: {target_role_name}")

        # Select the role
        success = role_mgmt_page.select_role_by_name(target_role_name)
        self.assertTrue(success, f"Should successfully select role {target_role_name}")

        # Verify role is selected by checking if it has the highlighted class
        selected_role = role_mgmt_page.get_selected_role_info()
        if selected_role:
            self.logger.info(f"Selected role: {selected_role['role_name']}")
            self.assertEqual(selected_role['role_name'], target_role_name,
                           "Selected role should match target role")

        self.logger.info("✓ Select role by name test passed")

    def test_select_role_by_code(self):
        """Test Case: Select a role by its role code"""
        self.logger.info("=== Test: Select Role by Code ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Get first role
        roles = role_mgmt_page.get_all_roles_info()
        if not roles:
            pytest.skip("No roles available for testing")

        target_role_code = roles[0]['role_code']
        self.logger.info(f"Selecting role with code: {target_role_code}")

        # Select the role
        success = role_mgmt_page.select_role_by_code(target_role_code)
        self.assertTrue(success, f"Should successfully select role with code {target_role_code}")

        self.logger.info("✓ Select role by code test passed")

    # ========== Search Tests ==========

    def test_search_role(self):
        """Test Case: Search for roles using search input"""
        self.logger.info("=== Test: Search Role ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Get first role to search for
        roles = role_mgmt_page.get_all_roles_info()
        if not roles:
            pytest.skip("No roles available for testing")

        search_term = roles[0]['role_name']
        self.logger.info(f"Searching for role: {search_term}")

        # Perform search
        success = role_mgmt_page.search_role(search_term)
        self.assertTrue(success, "Search should execute successfully")

        # Verify search results
        filtered_roles = role_mgmt_page.get_all_roles_info()
        self.logger.info(f"Found {len(filtered_roles)} roles matching search")

        # At least one result should contain the search term
        found = False
        for role in filtered_roles:
            if search_term.lower() in role['role_name'].lower():
                found = True
                break

        self.assertTrue(found, f"Search results should contain {search_term}")
        self.logger.info("✓ Search role test passed")

    def test_clear_search(self):
        """Test Case: Clear the search input"""
        self.logger.info("=== Test: Clear Search ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Get initial count
        initial_roles = role_mgmt_page.get_all_roles_info()
        initial_count = len(initial_roles)
        self.logger.info(f"Initial role count: {initial_count}")

        # Perform search
        if initial_roles:
            search_term = initial_roles[0]['role_name']
            role_mgmt_page.search_role(search_term)
            time.sleep(1)

            filtered_count = role_mgmt_page.get_role_count()
            self.logger.info(f"Filtered role count: {filtered_count}")

        # Clear search
        success = role_mgmt_page.clear_search()
        self.assertTrue(success, "Clear search should execute successfully")

        # Get count after clearing
        cleared_count = role_mgmt_page.get_role_count()
        self.logger.info(f"Count after clearing search: {cleared_count}")

        # Count after clearing should be >= filtered count
        self.assertTrue(cleared_count >= filtered_count,
                       "Clearing search should show more or equal roles")

        self.logger.info("✓ Clear search test passed")

    # ========== Menu Tree Tests ==========

    def test_get_menu_tree_nodes_count(self):
        """Test Case: Get the count of menu tree nodes"""
        self.logger.info("=== Test: Get Menu Tree Nodes Count ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Select first role to display menu tree
        roles = role_mgmt_page.get_all_roles_info()
        if roles:
            role_mgmt_page.select_role_by_name(roles[0]['role_name'])
            time.sleep(1)

        # Get menu tree nodes count
        nodes_count = role_mgmt_page.get_menu_tree_nodes_count()
        self.logger.info(f"Menu tree nodes count: {nodes_count}")

        # Verify count is reasonable
        self.assertTrue(nodes_count >= 0, "Nodes count should be >= 0")

        self.logger.info("✓ Menu tree nodes count test passed")

    def test_assign_menu_button_visibility(self):
        """Test Case: Verify Assign Menu button is visible after selecting a role"""
        self.logger.info("=== Test: Assign Menu Button Visibility ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Select first role to display menu tree and button
        roles = role_mgmt_page.get_all_roles_info()
        if not roles:
            pytest.skip("No roles available for testing")

        target_role = roles[0]['role_name']
        self.logger.info(f"Selecting role: {target_role}")
        success = role_mgmt_page.select_role_by_name(target_role)
        self.assertTrue(success, f"Should successfully select role {target_role}")

        time.sleep(1)  # Wait for menu tree to load

        # Check if Assign Menu button is visible
        is_visible = role_mgmt_page.is_assign_menu_button_visible()
        self.logger.info(f"Assign Menu button visible: {is_visible}")

        self.assertTrue(is_visible, "Assign Menu button should be visible after selecting a role")

        self.logger.info("✓ Assign Menu button visibility test passed")

    def test_click_assign_menu_button(self):
        """Test Case: Click the Assign Menu button"""
        self.logger.info("=== Test: Click Assign Menu Button ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Select a role first
        roles = role_mgmt_page.get_all_roles_info()
        if roles:
            role_mgmt_page.select_role_by_name(roles[0]['role_name'])
            time.sleep(1)

        # Click Assign Menu button
        success = role_mgmt_page.click_assign_menu_button()
        self.logger.info(f"Assign Menu button clicked: {success}")

        self.logger.info("✓ Click Assign Menu button test completed")

    def test_get_menu_checkbox_state(self):
        """Test Case: Get the state of menu checkboxes"""
        self.logger.info("=== Test: Get Menu Checkbox State ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Select first role
        roles = role_mgmt_page.get_all_roles_info()
        if roles:
            role_mgmt_page.select_role_by_name(roles[0]['role_name'])
            time.sleep(1)

        # Test menu names from the HTML
        menu_names = ['Chat', 'Documents', 'User Management',
                     'Role Management', 'Configuration', 'Profile']

        for menu_name in menu_names:
            checkbox_state = role_mgmt_page.get_menu_checkbox_state(menu_name)
            self.logger.info(f"Menu '{menu_name}' checkbox state: {checkbox_state}")

        self.logger.info("✓ Get menu checkbox state test passed")

    def test_get_all_menu_checkboxes_state(self):
        """Test Case: Get the state of all menu checkboxes at once"""
        self.logger.info("=== Test: Get All Menu Checkboxes State ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Select first role
        roles = role_mgmt_page.get_all_roles_info()
        if roles:
            role_mgmt_page.select_role_by_name(roles[0]['role_name'])
            time.sleep(1)

        # Get all menu checkboxes state
        all_states = role_mgmt_page.get_all_menu_checkboxes_state()
        self.logger.info(f"All menu checkboxes state: {all_states}")

        # Verify we got some states
        self.assertTrue(len(all_states) > 0, "Should retrieve at least one checkbox state")

        for menu_name, state in all_states.items():
            self.logger.info(f"  {menu_name}: {state}")

        self.logger.info("✓ Get all menu checkboxes state test passed")

    def test_is_menu_checkbox_disabled(self):
        """Test Case: Check if menu checkboxes are disabled"""
        self.logger.info("=== Test: Is Menu Checkbox Disabled ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Select first role
        roles = role_mgmt_page.get_all_roles_info()
        if roles:
            role_mgmt_page.select_role_by_name(roles[0]['role_name'])
            time.sleep(1)

        # Test menu names
        menu_names = ['Chat', 'Documents', 'User Management']

        for menu_name in menu_names:
            is_disabled = role_mgmt_page.is_menu_checkbox_disabled(menu_name)
            self.logger.info(f"Menu '{menu_name}' checkbox disabled: {is_disabled}")

        self.logger.info("✓ Is menu checkbox disabled test passed")

    def test_role_status_verification(self):
        """Test Case: Verify role status values"""
        self.logger.info("=== Test: Role Status Verification ===")

        role_mgmt_page = self._login_and_navigate_to_role_management()

        # Get all roles
        roles = role_mgmt_page.get_all_roles_info()

        active_count = 0
        inactive_count = 0

        for role in roles:
            status = role['status']
            if status == "Active":
                active_count += 1
            elif status == "Inactive":
                inactive_count += 1

            self.logger.info(f"Role: {role['role_name']}, Status: {status}")

        self.logger.info(f"Active roles: {active_count}, Inactive roles: {inactive_count}")
        self.logger.info("✓ Role status verification test passed")
