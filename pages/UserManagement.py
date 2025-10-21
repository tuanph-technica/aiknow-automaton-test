"""
UserManagement Page Object Module

This module provides a comprehensive page object for the User Management page,
including user list, search, filtering, add/edit user functionality, and pagination.
"""

import time
from typing import List, Optional, Dict, Tuple
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from base.base_driver import BaseDriver


class UserManagement(BaseDriver):
    """
    Page Object for User Management page.

    Inherits from BaseDriver to provide Selenium WebDriver utilities
    and custom waiting/interaction methods.
    """

    # ========== Page Locators ==========

    # Main page elements
    USER_LIST_TAG = (By.TAG_NAME, "app-user-list")
    PAGE_TITLE = (By.CSS_SELECTOR, "h2.page-title")
    ADD_USER_BUTTON = (By.CSS_SELECTOR, "button.btn-primary")

    # Search and Filters
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Search user by name or email']")
    ROLE_FILTER_SELECT = (By.CSS_SELECTOR, "select.form-select.choices__input[multiple]")
    STATUS_FILTER_SELECT = (By.XPATH, "//select[@data-plugin='choices' and not(@multiple)]")
    DATE_RANGE_INPUT = (By.CSS_SELECTOR, ".flatpickr-range input[data-input]")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".btn-primary.filter-btn")
    RESET_BUTTON = (By.CSS_SELECTOR, ".btn-outline-gray.filter-btn")

    # User List Table
    USER_TABLE = (By.CSS_SELECTOR, "table.table")
    TABLE_ROWS = (By.CSS_SELECTOR, "table.table tbody tr")
    TABLE_HEADER = (By.CSS_SELECTOR, "table.table thead tr")

    # Column indices (0-based)
    COL_AVATAR = 0
    COL_USERNAME = 1
    COL_NAME_EN = 2
    COL_NAME_JP = 3
    COL_EMAIL = 4
    COL_ROLE = 5
    COL_STATUS = 6
    COL_CREATED_DATE = 7
    COL_ACTION = 8

    # Pagination
    PAGINATOR = (By.CSS_SELECTOR, "mat-paginator")
    PAGINATION_RANGE = (By.CSS_SELECTOR, ".mat-mdc-paginator-range-label")
    NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-next")
    PREV_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-previous")
    FIRST_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-first")
    LAST_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-last")
    PAGE_SIZE_SELECT = (By.CSS_SELECTOR, ".mat-mdc-paginator-page-size-select")

    # ========== Add User Modal Locators ==========

    ADD_USER_MODAL = (By.ID, "modal-user-add")
    ADD_USER_MODAL_TITLE = (By.CSS_SELECTOR, "#modal-user-add .modal-title")
    ADD_USER_CLOSE_BUTTON = (By.CSS_SELECTOR, "#modal-user-add .btn-close")

    # Add User Form Fields
    ADD_USERNAME_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='username']")
    ADD_EMAIL_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='email']")
    ADD_FIRST_NAME_EN_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='firstNameEn']")
    ADD_LAST_NAME_EN_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='lastNameEn']")
    ADD_FIRST_NAME_JP_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='firstName']")
    ADD_LAST_NAME_JP_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='lastName']")
    ADD_DOB_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='dateOfBirth']")
    ADD_ROLES_SELECT = (By.CSS_SELECTOR, "select[formcontrolname='roles']")

    # Gender radio buttons
    ADD_GENDER_MALE_RADIO = (By.CSS_SELECTOR, "input[formcontrolname='gender'][value='MALE']")
    ADD_GENDER_FEMALE_RADIO = (By.CSS_SELECTOR, "input[formcontrolname='gender'][value='FEMALE']")
    ADD_GENDER_OTHER_RADIO = (By.CSS_SELECTOR, "input[formcontrolname='gender'][value='OTHER']")

    # Add User Modal Buttons
    ADD_USER_CANCEL_BUTTON = (By.CSS_SELECTOR, "#modal-user-add .btn-outline-gray")
    ADD_USER_SUBMIT_BUTTON = (By.CSS_SELECTOR, "#modal-user-add .btn-primary")

    # Validation messages
    ADD_USERNAME_ERROR = (By.CSS_SELECTOR, "input[formcontrolname='username'] ~ .invalid-feedback")
    ADD_EMAIL_ERROR = (By.CSS_SELECTOR, "input[formcontrolname='email'] ~ .invalid-feedback")

    # ========== Edit User Modal Locators ==========

    EDIT_USER_MODAL = (By.ID, "modal-user-edit")
    EDIT_USER_MODAL_TITLE = (By.CSS_SELECTOR, "#modal-user-edit .modal-title")
    EDIT_USER_CLOSE_BUTTON = (By.CSS_SELECTOR, "#modal-user-edit .btn-close")

    # Edit User Sections
    EDIT_PROFILE_SECTION = (By.CSS_SELECTOR, ".card-body:has(h5:contains('Profile Information'))")
    EDIT_CONTACT_SECTION = (By.CSS_SELECTOR, ".card-body:has(h5:contains('Contact Information'))")
    EDIT_ROLES_SECTION = (By.CSS_SELECTOR, ".card-body:has(h5:contains('Roles'))")

    # Edit buttons for each section
    EDIT_PROFILE_BUTTON = (By.XPATH, "//h5[contains(text(), 'Profile Information')]/following-sibling::button")
    EDIT_CONTACT_BUTTON = (By.XPATH, "//h5[contains(text(), 'Contact Information')]/following-sibling::button")
    EDIT_ROLES_BUTTON = (By.XPATH, "//h5[contains(text(), 'Roles')]/following-sibling::button")

    # Profile Information fields (view mode)
    PROFILE_USERNAME_VALUE = (By.XPATH, "//td[text()='Username']/following-sibling::td")
    PROFILE_FIRST_NAME_EN_VALUE = (By.XPATH, "//td[text()='First Name (En)']/following-sibling::td")
    PROFILE_LAST_NAME_EN_VALUE = (By.XPATH, "//td[text()='Last Name (En)']/following-sibling::td")
    PROFILE_FIRST_NAME_JP_VALUE = (By.XPATH, "//td[text()='First Name']/following-sibling::td")
    PROFILE_LAST_NAME_JP_VALUE = (By.XPATH, "//td[text()='Last Name']/following-sibling::td")
    PROFILE_GENDER_VALUE = (By.XPATH, "//td[text()='Gender']/following-sibling::td")
    PROFILE_DOB_VALUE = (By.XPATH, "//td[text()='Date of Birth']/following-sibling::td")

    # Contact Information fields (view mode)
    CONTACT_EMAIL_VALUE = (By.XPATH, "//td[text()='Email']/following-sibling::td")

    # Roles fields (view mode)
    ROLES_VALUE = (By.XPATH, "//td[text()='Roles']/following-sibling::td")

    # Edit User Modal Buttons
    EDIT_USER_CANCEL_BUTTON = (By.CSS_SELECTOR, "#modal-user-edit .btn-outline-gray")
    EDIT_USER_SAVE_BUTTON = (By.CSS_SELECTOR, "#modal-user-edit .btn-primary")

    # Status values
    STATUS_ACTIVE = "Active"
    STATUS_INACTIVE = "Inactive"

    # Gender values
    GENDER_MALE = "MALE"
    GENDER_FEMALE = "FEMALE"
    GENDER_OTHER = "OTHER"

    def __init__(self, driver):
        """
        Initialize UserManagement page object.

        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    # ========== Navigation Methods ==========

    def is_page_loaded(self) -> bool:
        """
        Check if User Management page is loaded.

        Returns:
            bool: True if page is loaded, False otherwise
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.USER_LIST_TAG))
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

    # ========== User List Methods ==========

    def get_user_count(self) -> int:
        """
        Get the total number of users displayed in the current page.

        Returns:
            int: Number of user rows in the table
        """
        try:
            rows = self.find_elements(*self.TABLE_ROWS)
            return len(rows)
        except NoSuchElementException:
            return 0

    def get_user_info(self, row_index: int) -> Optional[Dict[str, str]]:
        """
        Get user information from a specific table row.

        Args:
            row_index: Row index (0-based)

        Returns:
            dict: User information with keys: username, name_en, name_jp, email, role, status, created_date
            None: If row not found
        """
        try:
            rows = self.find_elements(*self.TABLE_ROWS)
            if row_index >= len(rows):
                return None

            row = rows[row_index]
            cells = row.find_elements(By.TAG_NAME, "td")

            if len(cells) < 9:
                return None

            user_info = {
                'username': cells[self.COL_USERNAME].text.strip(),
                'name_en': cells[self.COL_NAME_EN].text.strip(),
                'name_jp': cells[self.COL_NAME_JP].text.strip(),
                'email': cells[self.COL_EMAIL].text.strip(),
                'role': cells[self.COL_ROLE].text.strip(),
                'status': cells[self.COL_STATUS].text.strip(),
                'created_date': cells[self.COL_CREATED_DATE].text.strip()
            }

            return user_info

        except (NoSuchElementException, IndexError):
            return None

    def get_all_users_info(self) -> List[Dict[str, str]]:
        """
        Get information for all users in the current page.

        Returns:
            list: List of user information dictionaries
        """
        users = []
        user_count = self.get_user_count()

        for i in range(user_count):
            user_info = self.get_user_info(i)
            if user_info:
                users.append(user_info)

        return users

    def is_user_present(self, username: str) -> bool:
        """
        Check if a user with the given username is present in the current page.

        Args:
            username: Username to search for

        Returns:
            bool: True if user is found, False otherwise
        """
        users = self.get_all_users_info()
        return any(user['username'] == username for user in users)

    # ========== Search and Filter Methods ==========

    def search_by_name_or_email(self, search_term: str) -> bool:
        """
        Search for users by name or email.

        Args:
            search_term: Name or email to search for

        Returns:
            bool: True if search executed successfully
        """
        try:
            # Wait for any loading overlays to disappear
            time.sleep(0.5)

            # Wait for search input to be clickable and interactable
            search_input = self.wait_until_element_is_clickable(*self.SEARCH_INPUT)

            # Clear the input field
            search_input.clear()
            time.sleep(0.3)

            # Type the search term
            search_input.send_keys(search_term)

            # Wait for and click search button
            search_button = self.wait_until_element_is_clickable(*self.SEARCH_BUTTON)
            search_button.click()

            time.sleep(2)  # Wait for search results to load
            return True

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Search error: {type(e).__name__}: {str(e)}")
            return False

    def filter_by_role(self, roles: List[str]) -> bool:
        """
        Filter users by role(s). Supports multiple role selection.

        Args:
            roles: List of role names (e.g., ['System Admin', 'CEO', 'User'])

        Returns:
            bool: True if filter applied successfully
        """
        try:
            # Click the role select to open dropdown
            role_select = self.wait_until_element_is_clickable(*self.ROLE_FILTER_SELECT)

            # For Choices.js multi-select, we need to click on the visible dropdown
            choices_container = self.driver.find_element(By.CSS_SELECTOR, ".choices[data-type='select-multiple']")
            choices_container.click()
            time.sleep(0.5)

            # Select each role
            for role in roles:
                # Find and click the option with matching text
                option_xpath = f"//div[@class='choices__list choices__list--dropdown']//div[contains(@class, 'choices__item') and contains(text(), '{role}')]"
                option = self.driver.find_element(By.XPATH, option_xpath)
                option.click()
                time.sleep(0.3)

            # Click search button to apply filter
            search_button = self.wait_until_element_is_clickable(*self.SEARCH_BUTTON)
            search_button.click()

            time.sleep(2)  # Wait for filter results
            return True

        except (TimeoutException, NoSuchElementException) as e:
            return False

    def filter_by_status(self, status: str) -> bool:
        """
        Filter users by status (Active/Inactive).

        Args:
            status: Status value ('Active' or 'Inactive')

        Returns:
            bool: True if filter applied successfully
        """
        try:
            # Click the status select to open dropdown
            choices_container = self.driver.find_element(By.CSS_SELECTOR, ".choices[data-type='select-one']")
            choices_container.click()
            time.sleep(0.5)

            # Select the status option
            option_xpath = f"//div[@class='choices__list choices__list--dropdown']//div[contains(@class, 'choices__item') and text()='{status}']"
            option = self.driver.find_element(By.XPATH, option_xpath)
            option.click()

            # Click search button to apply filter
            search_button = self.wait_until_element_is_clickable(*self.SEARCH_BUTTON)
            search_button.click()

            time.sleep(2)  # Wait for filter results
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def filter_by_date_range(self, start_date: str, end_date: str) -> bool:
        """
        Filter users by created date range.

        Args:
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'

        Returns:
            bool: True if filter applied successfully
        """
        try:
            date_input = self.wait_until_element_is_clickable(*self.DATE_RANGE_INPUT)
            date_input.click()
            time.sleep(0.5)

            # Format: start_date to end_date
            date_range_str = f"{start_date} to {end_date}"
            date_input.clear()
            date_input.send_keys(date_range_str)
            date_input.send_keys(Keys.ENTER)

            # Click search button to apply filter
            search_button = self.wait_until_element_is_clickable(*self.SEARCH_BUTTON)
            search_button.click()

            time.sleep(2)  # Wait for filter results
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def reset_filters(self) -> bool:
        """
        Reset all filters to default values.

        Returns:
            bool: True if reset successful
        """
        try:
            reset_button = self.wait_until_element_is_clickable(*self.RESET_BUTTON)
            reset_button.click()

            time.sleep(2)  # Wait for page to reload with reset filters
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    # ========== Add User Modal Methods ==========

    def open_add_user_modal(self) -> bool:
        """
        Open the Add User modal dialog.

        Returns:
            bool: True if modal opened successfully
        """
        try:
            add_button = self.wait_until_element_is_clickable(*self.ADD_USER_BUTTON)
            add_button.click()

            # Wait for modal to appear
            self.wait.until(EC.visibility_of_element_located(self.ADD_USER_MODAL))
            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def fill_add_user_form(self, user_data: Dict[str, any]) -> bool:
        """
        Fill out the Add User form with provided data.

        Args:
            user_data: Dictionary with keys:
                - username (str, required)
                - email (str, required)
                - first_name_en (str, required)
                - last_name_en (str, required)
                - first_name_jp (str, required)
                - last_name_jp (str, required)
                - gender (str, required: 'MALE', 'FEMALE', or 'OTHER')
                - date_of_birth (str, required: 'YYYY-MM-DD')
                - roles (list, required: list of role names)

        Returns:
            bool: True if form filled successfully
        """
        try:
            # Username (required)
            print("Filling username...")
            username_input = self.wait_until_element_is_clickable(*self.ADD_USERNAME_INPUT)
            username_input.clear()
            username_input.send_keys(user_data['username'])
            time.sleep(0.3)

            # Email (required)
            print("Filling email...")
            email_input = self.wait_until_element_is_clickable(*self.ADD_EMAIL_INPUT)
            email_input.clear()
            email_input.send_keys(user_data['email'])
            time.sleep(0.3)

            # First Name EN (required)
            print("Filling first name EN...")
            first_name_en_input = self.wait_until_element_is_clickable(*self.ADD_FIRST_NAME_EN_INPUT)
            first_name_en_input.clear()
            first_name_en_input.send_keys(user_data['first_name_en'])
            time.sleep(0.3)

            # Last Name EN (required)
            print("Filling last name EN...")
            last_name_en_input = self.wait_until_element_is_clickable(*self.ADD_LAST_NAME_EN_INPUT)
            last_name_en_input.clear()
            last_name_en_input.send_keys(user_data['last_name_en'])
            time.sleep(0.3)

            # First Name JP (required based on HTML - must be Roman characters, 2-50 chars)
            print("Filling first name JP...")
            first_name_jp_input = self.wait_until_element_is_clickable(*self.ADD_FIRST_NAME_JP_INPUT)
            first_name_jp_input.clear()
            # Use Roman characters, not Japanese characters
            first_name_jp_input.send_keys(user_data.get('first_name_jp', 'Tesuto'))
            time.sleep(0.3)

            # Last Name JP (required based on HTML - must be Roman characters, 2-50 chars)
            print("Filling last name JP...")
            last_name_jp_input = self.wait_until_element_is_clickable(*self.ADD_LAST_NAME_JP_INPUT)
            last_name_jp_input.clear()
            # Use Roman characters, not Japanese characters
            last_name_jp_input.send_keys(user_data.get('last_name_jp', 'TestUser'))
            time.sleep(0.3)

            # Gender (required) - using ID-based selection
            print("Selecting gender...")
            gender = user_data.get('gender', 'MALE').upper()
            if gender == 'MALE':
                gender_radio = self.driver.find_element(By.ID, "profile-form-male")
            elif gender == 'FEMALE':
                gender_radio = self.driver.find_element(By.ID, "profile-form-famale")  # Note: typo in HTML
            else:
                gender_radio = self.wait_until_element_is_clickable(*self.ADD_GENDER_MALE_RADIO)

            # Click using JavaScript to ensure it works
            self.driver.execute_script("arguments[0].click();", gender_radio)
            time.sleep(0.3)

            # Date of Birth (required) - Flatpickr date picker (readonly field)
            print("Filling date of birth...")
            dob_input = self.wait_until_element_is_clickable(*self.ADD_DOB_INPUT)

            # Use JavaScript to set the value since it's readonly
            dob_value = user_data['date_of_birth'].replace('-', '/')  # Convert YYYY-MM-DD to YYYY/MM/DD
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                dob_input,
                dob_value
            )
            time.sleep(0.5)

            # Roles (required, multi-select with Choices.js)
            print("Selecting roles...")
            # Find the underlying hidden select element
            select_element = self.driver.find_element(By.CSS_SELECTOR, "select[formcontrolname='roles']")
            self.driver.execute_script("arguments[0].click()",select_element)

            all_items = self.driver.find_elements(By.CLASS_NAME, "choices__item--selectable")
            all_items[8].click()
            button_confirm = self.driver.find_element(By.XPATH, "//button[normalize-space()='Confirm']")
            button_confirm.click()
            return True


        except:
            return False




    def get_add_user_form_validation_errors(self) -> list:
        """
        Get any validation errors currently displayed on the Add User form.

        Returns:
            list: List of validation error messages
        """
        try:
            errors = []
            # Find all invalid-feedback elements that are displayed
            error_elements = self.driver.find_elements(By.CSS_SELECTOR, "#modal-user-add .invalid-feedback")
            for elem in error_elements:
                if elem.is_displayed():
                    errors.append(elem.text.strip())
            return errors
        except:
            return []

    def is_add_user_submit_button_enabled(self) -> bool:
        """
        Check if the Add User submit button is enabled.
        The button is only enabled when all required fields are filled.

        Returns:
            bool: True if button is enabled, False otherwise
        """
        try:
            submit_button = self.driver.find_element(*self.ADD_USER_SUBMIT_BUTTON)

            # Check if button is disabled via disabled attribute or class
            is_disabled = submit_button.get_attribute('disabled')
            button_classes = submit_button.get_attribute('class') or ''

            # Button is enabled if:
            # - disabled attribute is None or False
            # - doesn't have 'disabled' in class list
            is_enabled = (is_disabled is None or is_disabled == 'false') and 'disabled' not in button_classes.lower()

            return is_enabled

        except NoSuchElementException:
            return False

    def submit_add_user(self) -> bool:
        """
        Submit the Add User form by clicking the submit button.
        Note: Button must be enabled (all required fields filled) before clicking.

        Returns:
            bool: True if submission successful
        """
        try:
            # Wait a moment for form validation to complete
            time.sleep(1)

            # Check if button is enabled
            if not self.is_add_user_submit_button_enabled():
                # Button is disabled, likely due to validation errors
                return False

            submit_button = self.wait_until_element_is_clickable(*self.ADD_USER_SUBMIT_BUTTON)
            submit_button.click()

            # Wait for modal to close
            time.sleep(3)

            # Check if modal is closed
            try:
                modal = self.driver.find_element(*self.ADD_USER_MODAL)
                is_displayed = modal.is_displayed()
                return not is_displayed  # Return True if modal is no longer displayed
            except NoSuchElementException:
                return True  # Modal not found means it's closed

        except (TimeoutException, NoSuchElementException):
            return False

    def cancel_add_user(self) -> bool:
        """
        Cancel the Add User form by clicking the cancel button.

        Returns:
            bool: True if cancellation successful
        """
        try:
            cancel_button = self.wait_until_element_is_clickable(*self.ADD_USER_CANCEL_BUTTON)
            cancel_button.click()

            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def get_add_user_validation_error(self, field: str) -> str:
        """
        Get validation error message for a specific field in Add User form.

        Args:
            field: Field name ('username' or 'email')

        Returns:
            str: Error message text, empty string if no error
        """
        try:
            if field == 'username':
                error_element = self.driver.find_element(*self.ADD_USERNAME_ERROR)
            elif field == 'email':
                error_element = self.driver.find_element(*self.ADD_EMAIL_ERROR)
            else:
                return ""

            return error_element.text.strip() if error_element.is_displayed() else ""

        except NoSuchElementException:
            return ""

    # ========== Edit User Modal Methods ==========

    def open_edit_user_modal(self, username: str) -> bool:
        """
        Open the Edit User modal by clicking on the user's avatar or username.

        Args:
            username: Username of the user to edit

        Returns:
            bool: True if modal opened successfully
        """
        try:
            # Find the row with matching username
            rows = self.find_elements(*self.TABLE_ROWS)

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > self.COL_USERNAME:
                    row_username = cells[self.COL_USERNAME].text.strip()
                    if row_username == username:
                        # Click the username cell to open the edit modal
                        # (can also click on avatar in COL_AVATAR)
                        cells[self.COL_USERNAME].click()

                        # Wait for modal to appear using the actual modal structure
                        # The modal has class "modal-body" with "profile profile-modal" inside
                        modal_locator = (By.CSS_SELECTOR, ".modal-body .profile.profile-modal")
                        self.wait.until(EC.visibility_of_element_located(modal_locator))

                        time.sleep(1)
                        return True

            return False  # User not found

        except (TimeoutException, NoSuchElementException) as e:
            # Log the exception for debugging
            print(f"Exception in open_edit_user_modal: {type(e).__name__}: {str(e)}")
            return False

    def get_user_profile_data(self) -> Optional[Dict[str, str]]:
        """
        Get user profile data from the Edit User modal (view mode).

        Returns:
            dict: User profile data with keys: username, first_name_en, last_name_en,
                  first_name_jp, last_name_jp, gender, date_of_birth, email, roles
            None: If data cannot be retrieved
        """
        try:
            profile_data = {
                'username': self.driver.find_element(*self.PROFILE_USERNAME_VALUE).text.strip(),
                'first_name_en': self.driver.find_element(*self.PROFILE_FIRST_NAME_EN_VALUE).text.strip(),
                'last_name_en': self.driver.find_element(*self.PROFILE_LAST_NAME_EN_VALUE).text.strip(),
                'first_name_jp': self.driver.find_element(*self.PROFILE_FIRST_NAME_JP_VALUE).text.strip(),
                'last_name_jp': self.driver.find_element(*self.PROFILE_LAST_NAME_JP_VALUE).text.strip(),
                'gender': self.driver.find_element(*self.PROFILE_GENDER_VALUE).text.strip(),
                'date_of_birth': self.driver.find_element(*self.PROFILE_DOB_VALUE).text.strip(),
                'email': self.driver.find_element(*self.CONTACT_EMAIL_VALUE).text.strip(),
                'roles': self.driver.find_element(*self.ROLES_VALUE).text.strip()
            }

            return profile_data

        except NoSuchElementException:
            return None

    def click_edit_profile_button(self) -> bool:
        """
        Click the Edit button for Profile Information section.

        Returns:
            bool: True if button clicked successfully
        """
        try:
            edit_button = self.wait_until_element_is_clickable(*self.EDIT_PROFILE_BUTTON)
            edit_button.click()
            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def click_edit_contact_button(self) -> bool:
        """
        Click the Edit button for Contact Information section.

        Returns:
            bool: True if button clicked successfully
        """
        try:
            edit_button = self.wait_until_element_is_clickable(*self.EDIT_CONTACT_BUTTON)
            edit_button.click()
            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def click_edit_roles_button(self) -> bool:
        """
        Click the Edit button for Roles section.

        Returns:
            bool: True if button clicked successfully
        """
        try:
            edit_button = self.wait_until_element_is_clickable(*self.EDIT_ROLES_BUTTON)
            edit_button.click()
            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def save_edit_user(self) -> bool:
        """
        Save changes in the Edit User modal.

        Returns:
            bool: True if save successful
        """
        try:
            save_button = self.wait_until_element_is_clickable(*self.EDIT_USER_SAVE_BUTTON)
            save_button.click()

            time.sleep(2)  # Wait for save operation
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def cancel_edit_user(self) -> bool:
        """
        Cancel editing in the Edit User modal.

        Returns:
            bool: True if cancellation successful
        """
        try:
            cancel_button = self.wait_until_element_is_clickable(*self.EDIT_USER_CANCEL_BUTTON)
            cancel_button.click()

            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def close_edit_user_modal(self) -> bool:
        """
        Close the Edit User modal using the X button.

        Returns:
            bool: True if modal closed successfully
        """
        try:
            close_button = self.wait_until_element_is_clickable(*self.EDIT_USER_CLOSE_BUTTON)
            close_button.click()

            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    # ========== Pagination Methods ==========

    def get_pagination_info(self) -> Optional[Dict[str, int]]:
        """
        Get pagination information (current range and total).

        Returns:
            dict: Pagination info with keys: start, end, total
            None: If pagination info cannot be retrieved
        """
        try:
            # Wait for pagination element to be present
            time.sleep(1)
            range_element = self.driver.find_element(*self.PAGINATION_RANGE)
            range_text = range_element.text.strip()

            # Format: "1 – 10 of 1063" or "1 - 10 of 1063"
            # Handle both dash types (en-dash – and hyphen -)
            range_text = range_text.replace('–', '-')
            parts = range_text.split()

            if len(parts) >= 5:
                start = int(parts[0])
                end = int(parts[2])
                total = int(parts[4])

                return {
                    'start': start,
                    'end': end,
                    'total': total
                }

            return None

        except (NoSuchElementException, ValueError, IndexError) as e:
            # Try alternate method - check if there's pagination at all
            try:
                # Check if paginator exists
                self.driver.find_element(*self.PAGINATOR)
                # Paginator exists but can't parse range - might be single page
                return None
            except NoSuchElementException:
                # No paginator at all
                return None

    def go_to_next_page(self) -> bool:
        """
        Navigate to the next page.

        Returns:
            bool: True if navigation successful
        """
        try:
            next_button = self.wait_until_element_is_clickable(*self.NEXT_PAGE_BUTTON)

            # Check if button is enabled
            if 'disabled' in next_button.get_attribute('class'):
                return False

            next_button.click()
            time.sleep(2)  # Wait for page to load
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

            # Check if button is enabled
            if 'disabled' in prev_button.get_attribute('class'):
                return False

            prev_button.click()
            time.sleep(2)  # Wait for page to load
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

            # Check if button is enabled
            if 'disabled' in first_button.get_attribute('class'):
                return False

            first_button.click()
            time.sleep(2)  # Wait for page to load
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

            # Check if button is enabled
            if 'disabled' in last_button.get_attribute('class'):
                return False

            last_button.click()
            time.sleep(2)  # Wait for page to load
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def toggle_user_status(self, username: str) -> bool:
        """
        Toggle the active/inactive status of a user.

        Args:
            username: Username of the user whose status to toggle

        Returns:
            bool: True if toggle successful
        """
        try:
            # Find the row with matching username
            rows = self.find_elements(*self.TABLE_ROWS)

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) > self.COL_USERNAME:
                    row_username = cells[self.COL_USERNAME].text.strip()
                    if row_username == username:
                        # Find and click the toggle switch in the status column
                        status_cell = cells[self.COL_STATUS]
                        toggle_input = status_cell.find_element(By.CSS_SELECTOR, "input[type='checkbox']")

                        # Click using JavaScript to handle the custom toggle
                        self.driver.execute_script("arguments[0].click();", toggle_input)

                        # Wait for confirmation modal to appear
                        time.sleep(1)

                        # Handle confirmation modal if it appears
                        try:
                            # Wait for and click the confirm button in the modal
                            confirm_button_locator = (By.CSS_SELECTOR, "#modal-document-delete-confirm .btn-primary, .modal.show .btn-primary")
                            confirm_button = self.wait.until(EC.element_to_be_clickable(confirm_button_locator))
                            confirm_button.click()

                            # Wait for modal to disappear
                            time.sleep(1)
                        except TimeoutException:
                            # No confirmation modal appeared, which is fine
                            pass

                        return True

            return False  # User not found

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error in toggle_user_status: {type(e).__name__}: {str(e)}")
            return False
