"""
RoleManagement Page Object Module

This module provides a comprehensive page object for the Role Management page,
including role list, search, menu tree display, and menu assignment functionality.
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


class RoleManagement(BaseDriver):
    """
    Page Object for Role Management page.

    Inherits from BaseDriver to provide Selenium WebDriver utilities
    and custom waiting/interaction methods.
    """

    # ========== Page Locators ==========

    # Main page elements
    ROLE_MANAGEMENT_TAG = (By.TAG_NAME, "app-settings-role-management")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1.fs-4")

    # Role Section
    ROLE_SECTION_TITLE = (By.XPATH, "//h2[contains(text(), 'Role')]")
    ROLE_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search']")

    # Role Table
    ROLE_TABLE = (By.CSS_SELECTOR, "table.table")
    ROLE_TABLE_ROWS = (By.CSS_SELECTOR, "table.table tbody tr.role-item")
    ROLE_TABLE_HEADER = (By.CSS_SELECTOR, "table.table thead tr")

    # Column indices (0-based)
    COL_ROLE_NAME = 0
    COL_ROLE_CODE = 1
    COL_STATUS = 2

    # Menu Tree Section
    MENU_TREE_SECTION_TITLE = (By.XPATH, "//h2[contains(text(), 'Menu Tree')]")
    ASSIGN_MENU_BUTTON = (By.XPATH, "//button[contains(., 'Assign menu')]")

    # Menu Tree Elements
    MENU_TREE = (By.CSS_SELECTOR, "mat-tree")
    MENU_TREE_NODES = (By.CSS_SELECTOR, "mat-tree-node")
    SELECT_ALL_CHECKBOX = (By.ID, "role-checkbox-1")

    # Menu Tree Checkboxes - Note: IDs are dynamic, so we use label-based locators
    # These will be constructed dynamically in the methods below

    # Menu Tree Toggle Buttons (expand/collapse)
    MENU_TOGGLE_BUTTONS = (By.CSS_SELECTOR, "button[mat-icon-button][mattreenodetoggle]")

    # Status values
    STATUS_ACTIVE = "Active"
    STATUS_INACTIVE = "Inactive"

    def __init__(self, driver):
        """
        Initialize RoleManagement page object.

        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    # ========== Navigation Methods ==========

    def is_page_loaded(self) -> bool:
        """
        Check if Role Management page is loaded.

        Returns:
            bool: True if page is loaded, False otherwise
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.ROLE_MANAGEMENT_TAG))
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

    # ========== Role List Methods ==========

    def get_role_count(self) -> int:
        """
        Get the total number of roles displayed in the table.

        Returns:
            int: Number of role rows in the table
        """
        try:
            rows = self.find_elements(*self.ROLE_TABLE_ROWS)
            return len(rows)
        except NoSuchElementException:
            return 0

    def get_role_info(self, row_index: int) -> Optional[Dict[str, str]]:
        """
        Get role information from a specific table row.

        Args:
            row_index: Row index (0-based)

        Returns:
            dict: Role information with keys: role_name, role_code, status
            None: If row not found
        """
        try:
            rows = self.find_elements(*self.ROLE_TABLE_ROWS)
            if row_index >= len(rows):
                return None

            row = rows[row_index]
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) < 3:
                return None

            role_info = {
                'role_name': cells[self.COL_ROLE_NAME].text.strip(),
                'role_code': cells[self.COL_ROLE_CODE].text.strip(),
                'status': cells[self.COL_STATUS].text.strip()
            }

            return role_info

        except (NoSuchElementException, IndexError):
            return None

    def get_all_roles_info(self) -> List[Dict[str, str]]:
        """
        Get information for all roles in the table.

        Returns:
            list: List of role information dictionaries
        """
        roles = []
        role_count = self.get_role_count()

        for i in range(role_count):
            role_info = self.get_role_info(i)
            if role_info:
                roles.append(role_info)

        return roles

    def is_role_present(self, role_name: str) -> bool:
        """
        Check if a role with the given name is present in the table.

        Args:
            role_name: Role name to search for

        Returns:
            bool: True if role is found, False otherwise
        """
        roles = self.get_all_roles_info()
        return any(role['role_name'] == role_name for role in roles)

    def select_role_by_name(self, role_name: str) -> bool:
        """
        Select a role by clicking on its row.

        Args:
            role_name: Name of the role to select

        Returns:
            bool: True if role was selected successfully
        """
        try:
            rows = self.find_elements(*self.ROLE_TABLE_ROWS)

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > self.COL_ROLE_NAME:
                    row_role_name = cells[self.COL_ROLE_NAME].text.strip()
                    if row_role_name == role_name:
                        row.click()
                        time.sleep(1)
                        return True

            return False  # Role not found

        except (NoSuchElementException, TimeoutException):
            return False

    def select_role_by_code(self, role_code: str) -> bool:
        """
        Select a role by clicking on its row using role code.

        Args:
            role_code: Code of the role to select

        Returns:
            bool: True if role was selected successfully
        """
        try:
            rows = self.find_elements(*self.ROLE_TABLE_ROWS)

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > self.COL_ROLE_CODE:
                    row_role_code = cells[self.COL_ROLE_CODE].text.strip()
                    if row_role_code == role_code:
                        row.click()
                        time.sleep(1)
                        return True

            return False  # Role not found

        except (NoSuchElementException, TimeoutException):
            return False

    # ========== Search Methods ==========

    def search_role(self, search_term: str) -> bool:
        """
        Search for roles using the search input.

        Args:
            search_term: Search term to filter roles

        Returns:
            bool: True if search executed successfully
        """
        try:
            search_input = self.wait_until_element_is_clickable(*self.ROLE_SEARCH_INPUT)
            search_input.clear()
            time.sleep(0.3)
            search_input.send_keys(search_term)
            time.sleep(1)  # Wait for search to filter results
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def clear_search(self) -> bool:
        """
        Clear the role search input.

        Returns:
            bool: True if search cleared successfully
        """
        try:
            search_input = self.wait_until_element_is_clickable(*self.ROLE_SEARCH_INPUT)
            search_input.clear()
            time.sleep(1)  # Wait for results to reload
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    # ========== Menu Tree Methods ==========

    def get_menu_tree_nodes_count(self) -> int:
        """
        Get the total number of menu tree nodes displayed.

        Returns:
            int: Number of menu tree nodes
        """
        try:
            nodes = self.find_elements(*self.MENU_TREE_NODES)
            return len(nodes)
        except NoSuchElementException:
            return 0

    def is_assign_menu_button_visible(self) -> bool:
        """
        Check if Assign Menu button is visible.

        Returns:
            bool: True if button is visible, False otherwise
        """
        try:
            button = self.find_element(*self.ASSIGN_MENU_BUTTON)
            return button.is_displayed()
        except NoSuchElementException:
            return False

    def click_assign_menu_button(self) -> bool:
        """
        Click the Assign Menu button.

        Returns:
            bool: True if button clicked successfully
        """
        try:
            button = self.wait_until_element_is_clickable(*self.ASSIGN_MENU_BUTTON)
            button.click()
            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def get_menu_checkbox_state(self, menu_name: str) -> Optional[bool]:
        """
        Get the checked state of a menu checkbox.

        Args:
            menu_name: Name of the menu (e.g., 'Chat', 'Documents')

        Returns:
            bool: True if checked, False if unchecked, None if not found
        """
        try:
            # Find the mat-tree-node that contains the label with matching text
            # Then find the checkbox within that node
            tree_nodes = self.find_elements(*self.MENU_TREE_NODES)

            for node in tree_nodes:
                try:
                    label = node.find_element(By.CSS_SELECTOR, "label.mdc-label")
                    if label.text.strip() == menu_name:
                        # Found the correct node, now get the checkbox
                        checkbox = node.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                        is_checked = checkbox.is_selected()
                        return is_checked
                except NoSuchElementException:
                    continue

            # Menu not found
            return None

        except NoSuchElementException:
            return None

    def is_menu_checkbox_disabled(self, menu_name: str) -> Optional[bool]:
        """
        Check if a menu checkbox is disabled.

        Args:
            menu_name: Name of the menu (e.g., 'Chat', 'Documents')

        Returns:
            bool: True if disabled, False if enabled, None if not found
        """
        try:
            # Find the mat-tree-node that contains the label with matching text
            # Then find the checkbox within that node
            tree_nodes = self.find_elements(*self.MENU_TREE_NODES)

            for node in tree_nodes:
                try:
                    label = node.find_element(By.CSS_SELECTOR, "label.mdc-label")
                    if label.text.strip() == menu_name:
                        # Found the correct node, now get the checkbox
                        checkbox = node.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                        is_disabled = not checkbox.is_enabled()
                        return is_disabled
                except NoSuchElementException:
                    continue

            # Menu not found
            return None

        except NoSuchElementException:
            return None

    def expand_menu_tree_node(self, node_index: int) -> bool:
        """
        Expand a menu tree node by clicking its toggle button.

        Args:
            node_index: Index of the node to expand (0-based)

        Returns:
            bool: True if expanded successfully
        """
        try:
            toggle_buttons = self.find_elements(*self.MENU_TOGGLE_BUTTONS)
            if node_index >= len(toggle_buttons):
                return False

            toggle_button = toggle_buttons[node_index]

            # Check if already expanded (button shows chevron_down or is expanded)
            icon = toggle_button.find_element(By.TAG_NAME, "mat-icon")
            if icon.text.strip() == "expand_more":
                # Already expanded
                return True

            # Click to expand
            toggle_button.click()
            time.sleep(0.5)
            return True

        except (NoSuchElementException, IndexError):
            return False

    def get_all_menu_checkboxes_state(self) -> Dict[str, bool]:
        """
        Get the state of all menu checkboxes.

        Returns:
            dict: Dictionary mapping menu names to their checked state
        """
        menu_names = ['Chat', 'Documents', 'User Management',
                     'Role Management', 'Configuration', 'Profile']

        states = {}
        for menu_name in menu_names:
            state = self.get_menu_checkbox_state(menu_name)
            if state is not None:
                states[menu_name] = state

        return states

    def get_selected_role_info(self) -> Optional[Dict[str, str]]:
        """
        Get information about the currently selected role.

        Returns:
            dict: Role information if a role is selected
            None: If no role is selected
        """
        try:
            # Find the row with class 'table-gray-200' which indicates selection
            selected_row = self.find_element(By.CSS_SELECTOR, "table.table tbody tr.table-gray-200")
            cells = selected_row.find_elements(By.TAG_NAME, "td")

            if len(cells) < 3:
                return None

            role_info = {
                'role_name': cells[self.COL_ROLE_NAME].text.strip(),
                'role_code': cells[self.COL_ROLE_CODE].text.strip(),
                'status': cells[self.COL_STATUS].text.strip()
            }

            return role_info

        except NoSuchElementException:
            return None
