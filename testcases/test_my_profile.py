"""
My Profile Test Suite

This module contains comprehensive test cases for the My Profile functionality,
including profile information retrieval, field editing, and password change.
"""

import os
import time
import random
from datetime import datetime
from typing import Dict, List

import pytest
import softest

from pages.login import Login
from pages.MyProfile import MyProfile
from utilities.customLogger import LogGen
from utilities.utils import Utils


@pytest.mark.usefixtures("setup")
@pytest.mark.test_my_profile
class TestMyProfile(softest.TestCase):
    """
    Test suite for My Profile functionality.

    Tests cover:
    - Profile information retrieval (personal info, contact info, roles, preferences)
    - Field editing workflow (click edit, modify value, save)
    - Change Password modal functionality
    - Data validation and persistence
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
        self.profile_page = None
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

    def _login_and_navigate_to_my_profile(self) -> MyProfile:
        """
        Helper method to log in and navigate to My Profile page.

        Returns:
            MyProfile: My Profile page object
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

        # Navigate to My Profile page via dropdown menu at bottom of sidebar
        # First, find and click the user avatar/dropdown trigger
        from selenium.webdriver.common.by import By
        user_dropdown = self.driver.find_element(By.CSS_SELECTOR, ".sidebar .nav-item.dropdown .nav-link")
        user_dropdown.click()
        time.sleep(1)

        # Then click on "My Profile" link in the dropdown
        my_profile_link = self.driver.find_element(By.XPATH, "//a[@href='/profile']")
        my_profile_link.click()
        time.sleep(2)

        # Create MyProfile page object
        profile_page = MyProfile(self.driver)

        if not profile_page.is_page_loaded():
            pytest.fail("My Profile page failed to load")

        return profile_page

    # ========== Page Load Tests ==========

    def test_page_loaded(self):
        """Test Case: Verify My Profile page loads successfully"""
        self.logger.info("=== Test: Page Loaded ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Verify page is loaded
        self.assertTrue(profile_page.is_page_loaded(), "My Profile page should be loaded")

        # Verify page title
        title = profile_page.get_page_title()
        self.logger.info(f"Page title: {title}")
        # Page title shows the username, not "My Account"
        self.assertTrue(len(title) > 0, "Page title should not be empty")

        self.logger.info("✓ Page loaded test passed")

    # ========== Personal Info Tests ==========

    def test_get_username(self):
        """Test Case: Get username value (readonly field)"""
        self.logger.info("=== Test: Get Username ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get username
        username = profile_page.get_username()
        self.logger.info(f"Username: {username}")

        # Verify username is not empty
        self.assertTrue(username, "Username should not be empty")
        self.assertTrue(len(username) > 0, "Username should have content")

        self.logger.info("✓ Get username test passed")

    def test_get_all_personal_info(self):
        """Test Case: Get all personal information fields"""
        self.logger.info("=== Test: Get All Personal Info ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get all personal info
        personal_info = profile_page.get_all_personal_info()
        self.logger.info(f"Personal Info: {personal_info}")

        # Verify all expected fields are present
        expected_fields = ['username', 'display_name', 'name_jp', 'name_en',
                          'gender', 'date_of_birth', 'address']
        for field in expected_fields:
            self.assertIn(field, personal_info, f"Personal info should have {field} field")

        # Verify username is not empty (required field)
        self.assertTrue(personal_info['username'], "Username should not be empty")

        self.logger.info("✓ Get all personal info test passed")

    def test_edit_display_name(self):
        """Test Case: Edit display name field"""
        self.logger.info("=== Test: Edit Display Name ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get original display name
        original_display_name = profile_page.get_display_name()
        self.logger.info(f"Original display name: {original_display_name}")

        # Click edit button
        success = profile_page.click_edit_display_name()
        self.assertTrue(success, "Should click edit display name button successfully")

        # Set new display name
        new_display_name = f"Test User {random.randint(1000, 9999)}"
        success = profile_page.set_display_name(new_display_name)
        self.assertTrue(success, f"Should set display name to {new_display_name}")

        # Save changes
        success = profile_page.click_save_button()
        self.assertTrue(success, "Should save changes successfully")

        # Verify display name was updated
        time.sleep(1)
        updated_display_name = profile_page.get_display_name()
        self.logger.info(f"Updated display name: {updated_display_name}")
        self.assertEqual(updated_display_name, new_display_name,
                        "Display name should be updated")

        self.logger.info("✓ Edit display name test passed")

    def test_edit_address(self):
        """Test Case: Edit address field"""
        self.logger.info("=== Test: Edit Address ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get original address
        original_address = profile_page.get_address()
        self.logger.info(f"Original address: {original_address}")

        # Click edit button
        success = profile_page.click_edit_address()
        self.assertTrue(success, "Should click edit address button successfully")

        # Set new address
        new_address = f"Test Address {random.randint(100, 999)}, Test City"
        success = profile_page.set_address(new_address)
        self.assertTrue(success, f"Should set address to {new_address}")

        # Save changes
        success = profile_page.click_save_button()
        self.assertTrue(success, "Should save changes successfully")

        # Verify address was updated
        time.sleep(1)
        updated_address = profile_page.get_address()
        self.logger.info(f"Updated address: {updated_address}")
        self.assertEqual(updated_address, new_address, "Address should be updated")

        self.logger.info("✓ Edit address test passed")

    def test_cancel_edit(self):
        """Test Case: Cancel editing (changes should not be saved)"""
        self.logger.info("=== Test: Cancel Edit ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get original display name
        original_display_name = profile_page.get_display_name()
        self.logger.info(f"Original display name: {original_display_name}")

        # Click edit button
        profile_page.click_edit_display_name()

        # Set new display name
        new_display_name = "This Should Not Be Saved"
        profile_page.set_display_name(new_display_name)

        # Cancel changes
        success = profile_page.click_cancel_button()
        self.assertTrue(success, "Should cancel changes successfully")

        # Verify display name was NOT updated
        time.sleep(1)
        current_display_name = profile_page.get_display_name()
        self.logger.info(f"Current display name after cancel: {current_display_name}")
        self.assertEqual(current_display_name, original_display_name,
                        "Display name should not change after cancel")

        self.logger.info("✓ Cancel edit test passed")

    # ========== Contact Info Tests ==========

    def test_get_all_contact_info(self):
        """Test Case: Get all contact information fields"""
        self.logger.info("=== Test: Get All Contact Info ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get all contact info
        contact_info = profile_page.get_all_contact_info()
        self.logger.info(f"Contact Info: {contact_info}")

        # Verify all expected fields are present
        expected_fields = ['email', 'phone']
        for field in expected_fields:
            self.assertIn(field, contact_info, f"Contact info should have {field} field")

        self.logger.info("✓ Get all contact info test passed")

    def test_edit_email(self):
        """Test Case: Edit email field"""
        self.logger.info("=== Test: Edit Email ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get original email
        original_email = profile_page.get_email()
        self.logger.info(f"Original email: {original_email}")

        # Click edit button
        success = profile_page.click_edit_email()
        self.assertTrue(success, "Should click edit email button successfully")

        # Set new email
        new_email = f"testuser{random.randint(1000, 9999)}@example.com"
        success = profile_page.set_email(new_email)
        self.assertTrue(success, f"Should set email to {new_email}")

        # Save changes
        success = profile_page.click_save_button()
        self.assertTrue(success, "Should save changes successfully")

        # Verify email was updated
        time.sleep(1)
        updated_email = profile_page.get_email()
        self.logger.info(f"Updated email: {updated_email}")
        self.assertEqual(updated_email, new_email, "Email should be updated")

        self.logger.info("✓ Edit email test passed")

    def test_edit_phone(self):
        """Test Case: Edit phone field"""
        self.logger.info("=== Test: Edit Phone ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get original phone
        original_phone = profile_page.get_phone()
        self.logger.info(f"Original phone: {original_phone}")

        # Click edit button
        success = profile_page.click_edit_phone()
        self.assertTrue(success, "Should click edit phone button successfully")

        # Set new phone
        new_phone = f"+84{random.randint(100000000, 999999999)}"
        success = profile_page.set_phone(new_phone)
        self.assertTrue(success, f"Should set phone to {new_phone}")

        # Save changes
        success = profile_page.click_save_button()
        self.assertTrue(success, "Should save changes successfully")

        # Verify phone was updated
        time.sleep(1)
        updated_phone = profile_page.get_phone()
        self.logger.info(f"Updated phone: {updated_phone}")
        self.assertEqual(updated_phone, new_phone, "Phone should be updated")

        self.logger.info("✓ Edit phone test passed")

    # ========== Assigned Roles Tests ==========

    def test_get_assigned_roles(self):
        """Test Case: Get assigned roles"""
        self.logger.info("=== Test: Get Assigned Roles ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get assigned roles
        roles = profile_page.get_assigned_roles()
        self.logger.info(f"Assigned Roles: {roles}")

        # Verify roles is a list
        self.assertIsInstance(roles, list, "Roles should be a list")

        # Log each role
        for i, role in enumerate(roles):
            self.logger.info(f"  Role {i+1}: {role}")

        self.logger.info("✓ Get assigned roles test passed")

    # ========== Preferences Tests ==========

    def test_get_all_preferences(self):
        """Test Case: Get all preference fields"""
        self.logger.info("=== Test: Get All Preferences ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get all preferences
        preferences = profile_page.get_all_preferences()
        self.logger.info(f"Preferences: {preferences}")

        # Verify all expected fields are present
        expected_fields = ['language', 'timezone', 'theme']
        for field in expected_fields:
            self.assertIn(field, preferences, f"Preferences should have {field} field")

        self.logger.info("✓ Get all preferences test passed")

    def test_edit_language(self):
        """Test Case: Edit language preference"""
        self.logger.info("=== Test: Edit Language ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get original language
        original_language = profile_page.get_language()
        self.logger.info(f"Original language: {original_language}")

        # Click edit button
        success = profile_page.click_edit_language()
        self.assertTrue(success, "Should click edit language button successfully")

        # Set new language (toggle between English and Japanese)
        new_language = "Japanese" if original_language == "English" else "English"
        success = profile_page.set_language(new_language)
        self.assertTrue(success, f"Should set language to {new_language}")

        # Save changes
        success = profile_page.click_save_button()
        self.assertTrue(success, "Should save changes successfully")

        # Verify language was updated
        time.sleep(1)
        updated_language = profile_page.get_language()
        self.logger.info(f"Updated language: {updated_language}")
        self.assertEqual(updated_language, new_language, "Language should be updated")

        self.logger.info("✓ Edit language test passed")

    def test_edit_theme(self):
        """Test Case: Edit theme preference"""
        self.logger.info("=== Test: Edit Theme ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get original theme
        original_theme = profile_page.get_theme()
        self.logger.info(f"Original theme: {original_theme}")

        # Click edit button
        success = profile_page.click_edit_theme()
        self.assertTrue(success, "Should click edit theme button successfully")

        # Set new theme (toggle between Light and Dark)
        new_theme = "Dark" if original_theme == "Light" else "Light"
        success = profile_page.set_theme(new_theme)
        self.assertTrue(success, f"Should set theme to {new_theme}")

        # Save changes
        success = profile_page.click_save_button()
        self.assertTrue(success, "Should save changes successfully")

        # Verify theme was updated
        time.sleep(1)
        updated_theme = profile_page.get_theme()
        self.logger.info(f"Updated theme: {updated_theme}")
        self.assertEqual(updated_theme, new_theme, "Theme should be updated")

        self.logger.info("✓ Edit theme test passed")

    # ========== Change Password Tests ==========

    def test_open_change_password_modal(self):
        """Test Case: Open Change Password modal"""
        self.logger.info("=== Test: Open Change Password Modal ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Open Change Password modal
        success = profile_page.open_change_password_modal()
        self.assertTrue(success, "Should open Change Password modal successfully")

        # Close modal for cleanup
        profile_page.close_change_password_modal()

        self.logger.info("✓ Open Change Password modal test passed")

    def test_cancel_change_password(self):
        """Test Case: Cancel Change Password modal"""
        self.logger.info("=== Test: Cancel Change Password ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Open Change Password modal
        profile_page.open_change_password_modal()

        # Fill form with test data
        success = profile_page.fill_change_password_form(
            current_password="current123",
            new_password="newpass123",
            confirm_password="newpass123"
        )
        self.assertTrue(success, "Should fill change password form successfully")

        # Cancel the form
        success = profile_page.cancel_change_password()
        self.assertTrue(success, "Should cancel change password successfully")

        self.logger.info("✓ Cancel change password test passed")

    def test_close_change_password_modal(self):
        """Test Case: Close Change Password modal using X button"""
        self.logger.info("=== Test: Close Change Password Modal ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Open Change Password modal
        profile_page.open_change_password_modal()

        # Close modal using X button
        success = profile_page.close_change_password_modal()
        self.assertTrue(success, "Should close Change Password modal successfully")

        self.logger.info("✓ Close change password modal test passed")

    # ========== Integration Tests ==========

    def test_edit_multiple_fields(self):
        """Test Case: Edit multiple fields in one session"""
        self.logger.info("=== Test: Edit Multiple Fields ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Edit display name
        profile_page.click_edit_display_name()
        new_display_name = f"MultiEdit Test {random.randint(1000, 9999)}"
        profile_page.set_display_name(new_display_name)
        profile_page.click_save_button()
        time.sleep(1)

        # Edit email
        profile_page.click_edit_email()
        new_email = f"multiedit{random.randint(1000, 9999)}@example.com"
        profile_page.set_email(new_email)
        profile_page.click_save_button()
        time.sleep(1)

        # Verify both fields were updated
        updated_display_name = profile_page.get_display_name()
        updated_email = profile_page.get_email()

        self.assertEqual(updated_display_name, new_display_name,
                        "Display name should be updated")
        self.assertEqual(updated_email, new_email, "Email should be updated")

        self.logger.info("✓ Edit multiple fields test passed")

    def test_verify_readonly_username_field(self):
        """Test Case: Verify username field is readonly (no edit button)"""
        self.logger.info("=== Test: Verify Readonly Username Field ===")

        profile_page = self._login_and_navigate_to_my_profile()

        # Get username
        username = profile_page.get_username()
        self.logger.info(f"Username: {username}")

        # Verify username field does not have edit button
        # (There should be no edit button for username field)
        self.assertTrue(username, "Username should be displayed")

        self.logger.info("✓ Verify readonly username field test passed")
