"""
Configuration Page Object Module

This module provides a comprehensive page object for the Configuration (Parameter Config) page,
including chat generation parameters, parameter editing, and configuration history table.
"""

import time
from typing import List, Optional, Dict, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from base.base_driver import BaseDriver


class Configuration(BaseDriver):
    """
    Page Object for Configuration (Parameter Config) page.

    Inherits from BaseDriver to provide Selenium WebDriver utilities
    and custom waiting/interaction methods.
    """

    # ========== Page Locators ==========

    # Main page elements
    CONFIG_MAIN_TAG = (By.TAG_NAME, "app-parameter-config-main")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1.fs-4")

    # Tab Navigation
    TAB_NAV = (By.CSS_SELECTOR, "ul.tab-nav.nav-tabs")
    CHAT_GENERATION_TAB = (By.CSS_SELECTOR, "a[href='#tab-chat-generation']")

    # Parameter Sidebar (Form)
    PARAM_SIDEBAR = (By.CSS_SELECTOR, ".param-sidebar")
    PARAM_FORM = (By.CSS_SELECTOR, "form.card")
    PARAM_TABLE = (By.CSS_SELECTOR, "table.table")

    # Parameter Input Fields
    TEMPERATURE_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='temperature']")
    TOP_P_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='topP']")
    MAX_TOKENS_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='maxTokens']")
    TOP_K_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='topK']")

    # Edit Button
    EDIT_BUTTON = (By.XPATH, "//button[contains(text(), 'Edit')]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Update')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Cancel')]")

    # Configuration History Table
    HISTORY_TABLE = (By.CSS_SELECTOR, "table.mat-mdc-table")
    HISTORY_TABLE_ROWS = (By.CSS_SELECTOR, "table.mat-mdc-table tbody tr.mat-mdc-row")
    HISTORY_TABLE_HEADER = (By.CSS_SELECTOR, "table.mat-mdc-table thead tr")

    # Column indices (0-based)
    COL_CONFIG_DATE = 0
    COL_TEMPERATURE = 1
    COL_TOP_P = 2
    COL_MAX_TOKENS = 3
    COL_TOP_K = 4
    COL_CREATED_BY = 5

    # Pagination
    PAGINATOR = (By.CSS_SELECTOR, "mat-paginator")
    PAGINATION_RANGE = (By.CSS_SELECTOR, ".mat-mdc-paginator-range-label")
    NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-next")
    PREV_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-previous")
    FIRST_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-first")
    LAST_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-last")
    PAGE_SIZE_SELECT = (By.CSS_SELECTOR, ".mat-mdc-paginator-page-size-select")

    def __init__(self, driver):
        """
        Initialize Configuration page object.

        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    # ========== Navigation Methods ==========

    def is_page_loaded(self) -> bool:
        """
        Check if Configuration page is loaded.

        Returns:
            bool: True if page is loaded, False otherwise
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.CONFIG_MAIN_TAG))
            return True
        except TimeoutException:
            return False

    def get_page_title(self) -> str:
        """
        Get the page title.

        Returns:
            str: Page title text
        """
        try:
            title_element = self.find_element(*self.PAGE_TITLE)
            return title_element.text.strip()
        except NoSuchElementException:
            return ""

    # ========== Parameter Form Methods ==========

    def get_current_temperature(self) -> Optional[str]:
        """
        Get the current temperature value.

        Returns:
            str: Temperature value or None if not found
        """
        try:
            input_elem = self.find_element(*self.TEMPERATURE_INPUT)
            return input_elem.get_attribute('value') or input_elem.get_attribute('placeholder')
        except NoSuchElementException:
            return None

    def get_current_top_p(self) -> Optional[str]:
        """
        Get the current Top P value.

        Returns:
            str: Top P value or None if not found
        """
        try:
            input_elem = self.find_element(*self.TOP_P_INPUT)
            return input_elem.get_attribute('value') or input_elem.get_attribute('placeholder')
        except NoSuchElementException:
            return None

    def get_current_max_tokens(self) -> Optional[str]:
        """
        Get the current Max Tokens value.

        Returns:
            str: Max Tokens value or None if not found
        """
        try:
            input_elem = self.find_element(*self.MAX_TOKENS_INPUT)
            return input_elem.get_attribute('value') or input_elem.get_attribute('placeholder')
        except NoSuchElementException:
            return None

    def get_current_top_k(self) -> Optional[str]:
        """
        Get the current Top K value.

        Returns:
            str: Top K value or None if not found
        """
        try:
            input_elem = self.find_element(*self.TOP_K_INPUT)
            return input_elem.get_attribute('value') or input_elem.get_attribute('placeholder')
        except NoSuchElementException:
            return None

    def get_all_current_parameters(self) -> Dict[str, str]:
        """
        Get all current parameter values.

        Returns:
            dict: Dictionary with parameter names and values
        """
        return {
            'temperature': self.get_current_temperature() or '',
            'top_p': self.get_current_top_p() or '',
            'max_tokens': self.get_current_max_tokens() or '',
            'top_k': self.get_current_top_k() or ''
        }

    def is_edit_button_visible(self) -> bool:
        """
        Check if Edit button is visible.

        Returns:
            bool: True if visible, False otherwise
        """
        try:
            button = self.find_element(*self.EDIT_BUTTON)
            return button.is_displayed()
        except NoSuchElementException:
            return False

    def click_edit_button(self) -> bool:
        """
        Click the Edit button to enable parameter editing.

        Returns:
            bool: True if clicked successfully
        """
        try:
            button = self.wait_until_element_is_clickable(*self.EDIT_BUTTON)
            button.click()
            time.sleep(1)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def are_parameter_inputs_enabled(self) -> bool:
        """
        Check if parameter input fields are enabled (editable).

        Returns:
            bool: True if inputs are enabled, False otherwise
        """
        try:
            temp_input = self.find_element(*self.TEMPERATURE_INPUT)
            return temp_input.is_enabled()
        except NoSuchElementException:
            return False

    def set_temperature(self, value: str) -> bool:
        """
        Set the temperature value.

        Args:
            value: Temperature value to set

        Returns:
            bool: True if set successfully
        """
        try:
            input_elem = self.wait_until_element_is_clickable(*self.TEMPERATURE_INPUT)
            input_elem.clear()
            time.sleep(0.2)
            input_elem.send_keys(value)
            time.sleep(0.3)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def set_top_p(self, value: str) -> bool:
        """
        Set the Top P value.

        Args:
            value: Top P value to set

        Returns:
            bool: True if set successfully
        """
        try:
            input_elem = self.wait_until_element_is_clickable(*self.TOP_P_INPUT)
            input_elem.clear()
            time.sleep(0.2)
            input_elem.send_keys(value)
            time.sleep(0.3)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def set_max_tokens(self, value: str) -> bool:
        """
        Set the Max Tokens value.

        Args:
            value: Max Tokens value to set

        Returns:
            bool: True if set successfully
        """
        try:
            input_elem = self.wait_until_element_is_clickable(*self.MAX_TOKENS_INPUT)
            input_elem.clear()
            time.sleep(0.2)
            input_elem.send_keys(value)
            time.sleep(0.3)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def set_top_k(self, value: str) -> bool:
        """
        Set the Top K value.

        Args:
            value: Top K value to set

        Returns:
            bool: True if set successfully
        """
        try:
            input_elem = self.wait_until_element_is_clickable(*self.TOP_K_INPUT)
            input_elem.clear()
            time.sleep(0.2)
            input_elem.send_keys(value)
            time.sleep(0.3)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def update_parameters(self, params: Dict[str, str]) -> bool:
        """
        Update multiple parameters at once.

        Args:
            params: Dictionary with parameter names and values
                   Keys: temperature, top_p, max_tokens, top_k

        Returns:
            bool: True if all parameters updated successfully
        """
        success = True

        if 'temperature' in params:
            success = success and self.set_temperature(params['temperature'])

        if 'top_p' in params:
            success = success and self.set_top_p(params['top_p'])

        if 'max_tokens' in params:
            success = success and self.set_max_tokens(params['max_tokens'])

        if 'top_k' in params:
            success = success and self.set_top_k(params['top_k'])

        return success

    def click_save_button(self) -> bool:
        """
        Click the Save/Update button to save parameter changes.

        Returns:
            bool: True if clicked successfully
        """
        try:
            button = self.wait_until_element_is_clickable(*self.SAVE_BUTTON)
            button.click()
            time.sleep(2)  # Wait for save operation
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def click_cancel_button(self) -> bool:
        """
        Click the Cancel button to discard changes.

        Returns:
            bool: True if clicked successfully
        """
        try:
            button = self.wait_until_element_is_clickable(*self.CANCEL_BUTTON)
            button.click()
            time.sleep(1)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    # ========== Configuration History Table Methods ==========

    def get_history_count(self) -> int:
        """
        Get the total number of configuration history records in the current page.

        Returns:
            int: Number of history rows in the table
        """
        try:
            rows = self.find_elements(*self.HISTORY_TABLE_ROWS)
            return len(rows)
        except NoSuchElementException:
            return 0

    def get_history_record(self, row_index: int) -> Optional[Dict[str, str]]:
        """
        Get configuration history information from a specific table row.

        Args:
            row_index: Row index (0-based)

        Returns:
            dict: History record with keys: config_date, temperature, top_p,
                  max_tokens, top_k, created_by
            None: If row not found
        """
        try:
            rows = self.find_elements(*self.HISTORY_TABLE_ROWS)
            if row_index >= len(rows):
                return None

            row = rows[row_index]
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) < 6:
                return None

            record = {
                'config_date': cells[self.COL_CONFIG_DATE].text.strip(),
                'temperature': cells[self.COL_TEMPERATURE].text.strip(),
                'top_p': cells[self.COL_TOP_P].text.strip(),
                'max_tokens': cells[self.COL_MAX_TOKENS].text.strip(),
                'top_k': cells[self.COL_TOP_K].text.strip(),
                'created_by': cells[self.COL_CREATED_BY].text.strip()
            }

            return record

        except (NoSuchElementException, IndexError):
            return None

    def get_all_history_records(self) -> List[Dict[str, str]]:
        """
        Get all configuration history records from the current page.

        Returns:
            list: List of history record dictionaries
        """
        records = []
        history_count = self.get_history_count()

        for i in range(history_count):
            record = self.get_history_record(i)
            if record:
                records.append(record)

        return records

    def get_latest_history_record(self) -> Optional[Dict[str, str]]:
        """
        Get the most recent configuration history record (first row).

        Returns:
            dict: Latest history record or None if table is empty
        """
        return self.get_history_record(0)

    # ========== Pagination Methods ==========

    def get_pagination_info(self) -> Optional[Dict[str, int]]:
        """
        Get pagination information (current range and total).

        Returns:
            dict: Pagination info with keys: start, end, total
            None: If pagination info cannot be retrieved
        """
        try:
            time.sleep(1)
            range_element = self.find_element(*self.PAGINATION_RANGE)
            range_text = range_element.text.strip()

            # Format: "1-10 of 138 results."
            # Replace en-dash with hyphen for consistency
            range_text = range_text.replace('–', '-')

            # Extract numbers using split
            parts = range_text.split()

            if len(parts) >= 4:
                # Get start-end range
                range_part = parts[0].split('-')
                start = int(range_part[0])
                end = int(range_part[1])

                # Get total (remove 'results.' if present)
                total_str = parts[2].replace(',', '')
                total = int(total_str)

                return {
                    'start': start,
                    'end': end,
                    'total': total
                }

            return None

        except (NoSuchElementException, ValueError, IndexError):
            return None

    def go_to_next_page(self) -> bool:
        """
        Navigate to the next page.

        Returns:
            bool: True if navigation successful
        """
        try:
            next_button = self.wait_until_element_is_clickable(*self.NEXT_PAGE_BUTTON)

            # Check if button is disabled (check for exact class, not substring)
            button_classes = next_button.get_attribute('class').split()
            if 'mat-mdc-button-disabled' in button_classes:
                return False

            next_button.click()
            time.sleep(2)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def go_to_previous_page(self) -> bool:
        """
        Navigate to the previous page.

        Returns:
            bool: True if navigation successful
        """
        try:
            prev_button = self.wait_until_element_is_clickable(*self.PREV_PAGE_BUTTON)

            # Check if button is disabled (check for exact class, not substring)
            button_classes = prev_button.get_attribute('class').split()
            if 'mat-mdc-button-disabled' in button_classes:
                return False

            prev_button.click()
            time.sleep(2)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def go_to_first_page(self) -> bool:
        """
        Navigate to the first page.

        Returns:
            bool: True if navigation successful
        """
        try:
            first_button = self.wait_until_element_is_clickable(*self.FIRST_PAGE_BUTTON)

            # Check if button is disabled (check for exact class, not substring)
            button_classes = first_button.get_attribute('class').split()
            if 'mat-mdc-button-disabled' in button_classes:
                return False

            first_button.click()
            time.sleep(2)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def go_to_last_page(self) -> bool:
        """
        Navigate to the last page.

        Returns:
            bool: True if navigation successful
        """
        try:
            last_button = self.wait_until_element_is_clickable(*self.LAST_PAGE_BUTTON)

            # Check if button is disabled (check for exact class, not substring)
            button_classes = last_button.get_attribute('class').split()
            if 'mat-mdc-button-disabled' in button_classes:
                return False

            last_button.click()
            time.sleep(2)
            return True

        except (TimeoutException, NoSuchElementException):
            return False
