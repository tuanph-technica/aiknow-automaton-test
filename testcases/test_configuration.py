"""
Configuration Test Suite

This module contains comprehensive test cases for the Configuration (Parameter Config) functionality,
including parameter viewing, editing, history retrieval, and pagination.
"""

import os
import time
import random
from datetime import datetime
from typing import Dict, List

import pytest
import softest

from pages.login import Login
from pages.Configuration import Configuration
from utilities.customLogger import LogGen
from utilities.utils import Utils


@pytest.mark.usefixtures("setup")
@pytest.mark.test_configuration
class TestConfiguration(softest.TestCase):
    """
    Test suite for Configuration (Parameter Config) functionality.

    Tests cover:
    - Page loading and navigation
    - Parameter retrieval
    - Parameter editing workflow
    - Configuration history table
    - Pagination navigation
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
        self.config_page = None
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

    def _login_and_navigate_to_configuration(self) -> Configuration:
        """
        Helper method to log in and navigate to Configuration page.

        Returns:
            Configuration: Configuration page object
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

        # Navigate through Settings menu to Configuration
        settings_page = homepage.get_setting_menu()
        time.sleep(1)

        # Click on Configuration menu item
        settings_page.get_menu_by_name("Configuration")
        time.sleep(2)

        # Create Configuration page object
        config_page = Configuration(self.driver)

        if not config_page.is_page_loaded():
            pytest.fail("Configuration page failed to load")

        return config_page

    # ========== Page Loading Tests ==========

    def test_page_loads_successfully(self):
        """Test Case: Verify Configuration page loads successfully"""
        self.logger.info("=== Test: Page Loads Successfully ===")

        config_page = self._login_and_navigate_to_configuration()

        # Verify page is loaded
        is_loaded = config_page.is_page_loaded()
        self.assertTrue(is_loaded, "Configuration page should be loaded")

        self.logger.info("✓ Page loads successfully test passed")

    def test_get_page_title(self):
        """Test Case: Verify Configuration page title"""
        self.logger.info("=== Test: Get Page Title ===")

        config_page = self._login_and_navigate_to_configuration()

        # Get page title
        title = config_page.get_page_title()
        self.logger.info(f"Page title: {title}")

        # Verify title contains expected text
        self.assertIn("Parameter Config", title, "Page title should contain 'Parameter Config'")

        self.logger.info("✓ Page title test passed")

    # ========== Parameter Retrieval Tests ==========

    def test_get_current_parameters(self):
        """Test Case: Get current parameter values"""
        self.logger.info("=== Test: Get Current Parameters ===")

        config_page = self._login_and_navigate_to_configuration()

        # Get all current parameters
        params = config_page.get_all_current_parameters()
        self.logger.info(f"Current parameters: {params}")

        # Verify parameters dictionary has all keys
        self.assertIn('temperature', params, "Should have temperature parameter")
        self.assertIn('top_p', params, "Should have top_p parameter")
        self.assertIn('max_tokens', params, "Should have max_tokens parameter")
        self.assertIn('top_k', params, "Should have top_k parameter")

        self.logger.info("✓ Get current parameters test passed")

    def test_get_individual_parameters(self):
        """Test Case: Get individual parameter values"""
        self.logger.info("=== Test: Get Individual Parameters ===")

        config_page = self._login_and_navigate_to_configuration()

        # Get individual parameters
        temperature = config_page.get_current_temperature()
        top_p = config_page.get_current_top_p()
        max_tokens = config_page.get_current_max_tokens()
        top_k = config_page.get_current_top_k()

        self.logger.info(f"Temperature: {temperature}")
        self.logger.info(f"Top P: {top_p}")
        self.logger.info(f"Max Tokens: {max_tokens}")
        self.logger.info(f"Top K: {top_k}")

        # Verify at least one parameter has a value
        has_value = any([temperature, top_p, max_tokens, top_k])
        self.assertTrue(has_value, "At least one parameter should have a value")

        self.logger.info("✓ Get individual parameters test passed")

    # ========== Parameter Editing Tests ==========

    def test_edit_button_visibility(self):
        """Test Case: Verify Edit button is visible"""
        self.logger.info("=== Test: Edit Button Visibility ===")

        config_page = self._login_and_navigate_to_configuration()

        # Check if Edit button is visible
        is_visible = config_page.is_edit_button_visible()
        self.logger.info(f"Edit button visible: {is_visible}")

        self.assertTrue(is_visible, "Edit button should be visible")

        self.logger.info("✓ Edit button visibility test passed")

    def test_click_edit_button(self):
        """Test Case: Click Edit button and verify inputs become editable"""
        self.logger.info("=== Test: Click Edit Button ===")

        config_page = self._login_and_navigate_to_configuration()

        # Check initial state (inputs should be disabled)
        initial_enabled = config_page.are_parameter_inputs_enabled()
        self.logger.info(f"Inputs enabled before edit: {initial_enabled}")

        # Click Edit button
        success = config_page.click_edit_button()
        self.assertTrue(success, "Edit button should be clicked successfully")

        # Check if inputs are now enabled
        after_enabled = config_page.are_parameter_inputs_enabled()
        self.logger.info(f"Inputs enabled after edit: {after_enabled}")

        self.assertTrue(after_enabled, "Inputs should be enabled after clicking Edit")

        self.logger.info("✓ Click edit button test passed")

    def test_update_parameters(self):
        """Test Case: Update parameter values"""
        self.logger.info("=== Test: Update Parameters ===")

        config_page = self._login_and_navigate_to_configuration()

        # Click Edit button first
        config_page.click_edit_button()
        time.sleep(1)

        # Prepare test parameters
        test_params = {
            'temperature': '0.8',
            'top_p': '0.95',
            'max_tokens': '3000',
            'top_k': '8'
        }

        self.logger.info(f"Updating parameters with: {test_params}")

        # Update parameters
        success = config_page.update_parameters(test_params)
        self.assertTrue(success, "Parameters should be updated successfully")

        self.logger.info("✓ Update parameters test completed")

        # Note: We don't save to avoid changing actual configuration

    # ========== Configuration History Tests ==========

    def test_get_history_count(self):
        """Test Case: Get the count of configuration history records"""
        self.logger.info("=== Test: Get History Count ===")

        config_page = self._login_and_navigate_to_configuration()

        # Get history count
        history_count = config_page.get_history_count()
        self.logger.info(f"History record count: {history_count}")

        # Verify count is reasonable
        self.assertTrue(history_count >= 0, "History count should be >= 0")
        self.assertTrue(history_count <= 100, "History count should be <= 100 per page")

        self.logger.info("✓ History count test passed")

    def test_get_all_history_records(self):
        """Test Case: Get all configuration history records"""
        self.logger.info("=== Test: Get All History Records ===")

        config_page = self._login_and_navigate_to_configuration()

        # Get all history records
        records = config_page.get_all_history_records()
        self.logger.info(f"Retrieved {len(records)} history records")

        # Verify we got some records
        if len(records) > 0:
            # Verify each record has required fields
            for i, record in enumerate(records[:3]):  # Check first 3 records
                self.logger.info(f"Record {i+1}: {record['config_date']} - "
                               f"Temp={record['temperature']}, TopP={record['top_p']}, "
                               f"MaxTokens={record['max_tokens']}, TopK={record['top_k']}, "
                               f"By={record['created_by']}")

                self.assertIn('config_date', record, "Record should have config_date")
                self.assertIn('temperature', record, "Record should have temperature")
                self.assertIn('top_p', record, "Record should have top_p")
                self.assertIn('max_tokens', record, "Record should have max_tokens")
                self.assertIn('top_k', record, "Record should have top_k")
                self.assertIn('created_by', record, "Record should have created_by")

        self.logger.info("✓ Get all history records test passed")

    def test_get_latest_history_record(self):
        """Test Case: Get the most recent configuration history record"""
        self.logger.info("=== Test: Get Latest History Record ===")

        config_page = self._login_and_navigate_to_configuration()

        # Get latest record
        latest = config_page.get_latest_history_record()

        if latest:
            self.logger.info(f"Latest record: {latest['config_date']} - "
                           f"Temp={latest['temperature']}, TopP={latest['top_p']}, "
                           f"MaxTokens={latest['max_tokens']}, TopK={latest['top_k']}")

            # Verify latest record has all required fields
            self.assertIn('config_date', latest, "Latest record should have config_date")
            self.assertIn('temperature', latest, "Latest record should have temperature")
            self.assertIn('created_by', latest, "Latest record should have created_by")
        else:
            self.logger.info("No history records found")

        self.logger.info("✓ Get latest history record test passed")

    def test_get_specific_history_record(self):
        """Test Case: Get a specific history record by index"""
        self.logger.info("=== Test: Get Specific History Record ===")

        config_page = self._login_and_navigate_to_configuration()

        # Get first record (index 0)
        record = config_page.get_history_record(0)

        if record:
            self.logger.info(f"Record at index 0: {record}")

            # Verify record structure
            self.assertIsInstance(record, dict, "Record should be a dictionary")
            self.assertTrue(len(record) > 0, "Record should not be empty")
        else:
            self.logger.info("No record found at index 0")

        self.logger.info("✓ Get specific history record test passed")

    # ========== Pagination Tests ==========

    def test_get_pagination_info(self):
        """Test Case: Get pagination information"""
        self.logger.info("=== Test: Get Pagination Info ===")

        config_page = self._login_and_navigate_to_configuration()

        # Get pagination info
        pagination_info = config_page.get_pagination_info()

        if pagination_info:
            self.logger.info(f"Pagination: {pagination_info['start']} – {pagination_info['end']} "
                           f"of {pagination_info['total']}")

            # Verify pagination info structure
            self.assertIn('start', pagination_info, "Should have start")
            self.assertIn('end', pagination_info, "Should have end")
            self.assertIn('total', pagination_info, "Should have total")

            # Verify values make sense
            self.assertTrue(pagination_info['start'] >= 1, "Start should be >= 1")
            self.assertTrue(pagination_info['end'] >= pagination_info['start'],
                          "End should be >= start")
            self.assertTrue(pagination_info['total'] >= pagination_info['end'],
                          "Total should be >= end")
        else:
            self.logger.info("Pagination info not available (single page)")

        self.logger.info("✓ Pagination info test passed")

    def test_pagination_navigation(self):
        """Test Case: Test pagination navigation (next, previous, first, last)"""
        self.logger.info("=== Test: Pagination Navigation ===")

        config_page = self._login_and_navigate_to_configuration()

        # Get initial pagination info
        initial_info = config_page.get_pagination_info()

        if not initial_info:
            self.logger.info("Only one page available, skipping navigation test")
            pytest.skip("Not enough records for pagination testing")

        self.logger.info(f"Initial page: {initial_info}")

        # Check if there are multiple pages
        if initial_info['total'] <= initial_info['end']:
            self.logger.info("Only one page available, skipping navigation test")
            pytest.skip("Not enough records for pagination testing")

        # Test next page
        self.logger.info("Testing next page navigation...")
        success = config_page.go_to_next_page()
        self.assertTrue(success, "Should navigate to next page")

        next_page_info = config_page.get_pagination_info()
        if next_page_info:
            self.logger.info(f"Next page: {next_page_info}")
            self.assertGreater(next_page_info['start'], initial_info['start'],
                             "Next page should have higher start value")

        # Test previous page
        self.logger.info("Testing previous page navigation...")
        success = config_page.go_to_previous_page()
        self.assertTrue(success, "Should navigate to previous page")

        prev_page_info = config_page.get_pagination_info()
        if prev_page_info:
            self.logger.info(f"Previous page: {prev_page_info}")
            self.assertEqual(prev_page_info['start'], initial_info['start'],
                           "Should return to initial page")

        self.logger.info("✓ Pagination navigation test passed")
