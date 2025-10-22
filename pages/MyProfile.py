"""
MyProfile Page Object Module

This module provides a comprehensive page object for the My Profile page,
including profile information display, editing profile fields, changing password,
and managing preferences.
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


class MyProfile(BaseDriver):
    """
    Page Object for My Profile page.

    Inherits from BaseDriver to provide Selenium WebDriver utilities
    and custom waiting/interaction methods.
    """

    # ========== Page Locators ==========

    # Main page elements
    PROFILE_MAIN_TAG = (By.TAG_NAME, "app-profile-my-account")
    PAGE_TITLE = (By.CSS_SELECTOR, "h1.fs-4")

    # Profile Sections
    PERSONAL_INFO_SECTION = (By.XPATH, "//h5[contains(text(), 'Personal Info')]")
    CONTACT_INFO_SECTION = (By.XPATH, "//h5[contains(text(), 'Contact Info')]")
    ASSIGNED_ROLES_SECTION = (By.XPATH, "//h5[contains(text(), 'Assigned Roles')]")
    PREFERENCES_SECTION = (By.XPATH, "//h5[contains(text(), 'Preferences')]")

    # Personal Info Fields (view mode) - Using contains() for flexibility
    USERNAME_VALUE = (By.XPATH, "//td[contains(text(), 'Username')]/following-sibling::td[1]")
    DISPLAY_NAME_VALUE = (By.XPATH, "//td[contains(text(), 'Display name')]/following-sibling::td[1]")
    NAME_JP_VALUE = (By.XPATH, "//td[contains(text(), 'Name (JP)')]/following-sibling::td[1]")
    NAME_EN_VALUE = (By.XPATH, "//td[contains(text(), 'Name (EN)')]/following-sibling::td[1]")
    GENDER_VALUE = (By.XPATH, "//td[contains(text(), 'Gender')]/following-sibling::td[1]")
    DOB_VALUE = (By.XPATH, "//td[contains(text(), 'Date of birth')]/following-sibling::td[1]")
    ADDRESS_VALUE = (By.XPATH, "//td[contains(text(), 'Address')]/following-sibling::td[1]")

    # Contact Info Fields (view mode) - Using contains() for flexibility
    EMAIL_VALUE = (By.XPATH, "//td[contains(text(), 'Email')]/following-sibling::td[1]")
    PHONE_VALUE = (By.XPATH, "//td[contains(text(), 'Phone')]/following-sibling::td[1]")

    # Assigned Roles Fields (view mode) - Get all role cells
    ROLES_VALUE = (By.XPATH, "//h5[contains(text(), 'Assigned Roles')]/ancestor::div[@class='card-header']/following-sibling::div//td")

    # Preferences Fields (view mode) - Using contains() for flexibility
    LANGUAGE_VALUE = (By.XPATH, "//td[contains(text(), 'Language')]/following-sibling::td[1]")
    TIMEZONE_VALUE = (By.XPATH, "//td[contains(text(), 'Time Zone')]/following-sibling::td[1]")
    THEME_VALUE = (By.XPATH, "//td[contains(text(), 'Theme')]/following-sibling::td[1]")

    # Edit Buttons (pencil icons) - Using contains() for flexibility
    EDIT_DISPLAY_NAME_BUTTON = (By.XPATH, "//td[contains(text(), 'Display name')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_NAME_JP_BUTTON = (By.XPATH, "//td[contains(text(), 'Name (JP)')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_NAME_EN_BUTTON = (By.XPATH, "//td[contains(text(), 'Name (EN)')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_GENDER_BUTTON = (By.XPATH, "//td[contains(text(), 'Gender')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_DOB_BUTTON = (By.XPATH, "//td[contains(text(), 'Date of birth')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_ADDRESS_BUTTON = (By.XPATH, "//td[contains(text(), 'Address')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_EMAIL_BUTTON = (By.XPATH, "//td[contains(text(), 'Email')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_PHONE_BUTTON = (By.XPATH, "//td[contains(text(), 'Phone')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_LANGUAGE_BUTTON = (By.XPATH, "//td[contains(text(), 'Language')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_TIMEZONE_BUTTON = (By.XPATH, "//td[contains(text(), 'Time Zone')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
    EDIT_THEME_BUTTON = (By.XPATH, "//td[contains(text(), 'Theme')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")

    # Input Fields (edit mode) - using formcontrolname
    DISPLAY_NAME_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='displayName']")
    NAME_JP_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='nameJp']")
    NAME_EN_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='nameEn']")
    GENDER_SELECT = (By.CSS_SELECTOR, "select[formcontrolname='gender']")
    DOB_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='dateOfBirth']")
    ADDRESS_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='address']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='email']")
    PHONE_INPUT = (By.CSS_SELECTOR, "input[formcontrolname='phone']")
    LANGUAGE_SELECT = (By.CSS_SELECTOR, "select[formcontrolname='language']")
    TIMEZONE_SELECT = (By.CSS_SELECTOR, "select[formcontrolname='timeZone']")
    THEME_SELECT = (By.CSS_SELECTOR, "select[formcontrolname='theme']")

    # Save/Cancel Buttons (shown after clicking edit)
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Save')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Cancel')]")

    # Change Password Button and Modal
    CHANGE_PASSWORD_BUTTON = (By.XPATH, "//button[contains(text(), 'Change Password')]")
    CHANGE_PASSWORD_MODAL = (By.ID, "modal-change-password")
    CHANGE_PASSWORD_MODAL_TITLE = (By.CSS_SELECTOR, "#modal-change-password .modal-title")

    # Change Password Form Fields
    CURRENT_PASSWORD_INPUT = (By.CSS_SELECTOR, "#modal-change-password input[formcontrolname='currentPassword']")
    NEW_PASSWORD_INPUT = (By.CSS_SELECTOR, "#modal-change-password input[formcontrolname='newPassword']")
    CONFIRM_PASSWORD_INPUT = (By.CSS_SELECTOR, "#modal-change-password input[formcontrolname='confirmPassword']")

    # Change Password Modal Buttons
    CHANGE_PASSWORD_SUBMIT_BUTTON = (By.CSS_SELECTOR, "#modal-change-password .btn-primary")
    CHANGE_PASSWORD_CANCEL_BUTTON = (By.CSS_SELECTOR, "#modal-change-password .btn-outline-gray")
    CHANGE_PASSWORD_CLOSE_BUTTON = (By.CSS_SELECTOR, "#modal-change-password .btn-close")

    # Profile Tables
    PROFILE_TABLE = (By.CSS_SELECTOR, ".table-profile")

    def __init__(self, driver):
        """
        Initialize MyProfile page object.

        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    # ========== Navigation Methods ==========

    def is_page_loaded(self) -> bool:
        """
        Check if My Profile page is loaded.

        Returns:
            bool: True if page is loaded, False otherwise
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.PROFILE_MAIN_TAG))
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

    # ========== Helper Methods ==========

    def _get_field_value(self, field_label: str) -> Optional[str]:
        """
        Generic method to get field value by label using multiple strategies.

        Args:
            field_label: The label of the field (e.g., 'Username', 'Email')

        Returns:
            str: Field value or None if not found
        """
        try:
            # Strategy 1: Try contains with following-sibling
            try:
                element = self.driver.find_element(By.XPATH,
                    f"//td[contains(text(), '{field_label}')]/following-sibling::td[1]")
                value = element.text.strip()
                if value:
                    return value
            except:
                pass

            # Strategy 2: Try with parent tr and nth td
            try:
                element = self.driver.find_element(By.XPATH,
                    f"//td[contains(text(), '{field_label}')]/parent::tr/td[2]")
                value = element.text.strip()
                if value:
                    return value
            except:
                pass

            # Strategy 3: Try with table-profile class
            try:
                element = self.driver.find_element(By.XPATH,
                    f"//table[@class='table-profile']//td[contains(text(), '{field_label}')]/following-sibling::td[1]")
                value = element.text.strip()
                if value:
                    return value
            except:
                pass

            return None
        except Exception as e:
            return None

    # ========== Personal Info Methods ==========

    def get_username(self) -> Optional[str]:
        """
        Get the username value (readonly field).

        Returns:
            str: Username or None if not found
        """
        return self._get_field_value("Username")

    def get_display_name(self) -> Optional[str]:
        """
        Get the display name value.

        Returns:
            str: Display name or None if not found
        """
        return self._get_field_value("Display name")

    def get_name_jp(self) -> Optional[str]:
        """
        Get the Name (JP) value.

        Returns:
            str: Name (JP) or None if not found
        """
        return self._get_field_value("Name (JP)")

    def get_name_en(self) -> Optional[str]:
        """
        Get the Name (EN) value.

        Returns:
            str: Name (EN) or None if not found
        """
        return self._get_field_value("Name (EN)")

    def get_gender(self) -> Optional[str]:
        """
        Get the gender value.

        Returns:
            str: Gender or None if not found
        """
        return self._get_field_value("Gender")

    def get_date_of_birth(self) -> Optional[str]:
        """
        Get the date of birth value.

        Returns:
            str: Date of birth or None if not found
        """
        return self._get_field_value("Date of birth")

    def get_address(self) -> Optional[str]:
        """
        Get the address value.

        Returns:
            str: Address or None if not found
        """
        return self._get_field_value("Address")

    def get_all_personal_info(self) -> Dict[str, str]:
        """
        Get all personal information fields.

        Returns:
            dict: Personal info with keys: username, display_name, name_jp, name_en,
                  gender, date_of_birth, address
        """
        return {
            'username': self.get_username() or '',
            'display_name': self.get_display_name() or '',
            'name_jp': self.get_name_jp() or '',
            'name_en': self.get_name_en() or '',
            'gender': self.get_gender() or '',
            'date_of_birth': self.get_date_of_birth() or '',
            'address': self.get_address() or ''
        }

    # ========== Contact Info Methods ==========

    def get_email(self) -> Optional[str]:
        """
        Get the email value.

        Returns:
            str: Email or None if not found
        """
        return self._get_field_value("Email")

    def get_phone(self) -> Optional[str]:
        """
        Get the phone value.

        Returns:
            str: Phone or None if not found
        """
        return self._get_field_value("Phone")

    def get_all_contact_info(self) -> Dict[str, str]:
        """
        Get all contact information fields.

        Returns:
            dict: Contact info with keys: email, phone
        """
        return {
            'email': self.get_email() or '',
            'phone': self.get_phone() or ''
        }

    # ========== Assigned Roles Methods ==========

    def get_assigned_roles(self) -> List[str]:
        """
        Get all assigned roles.

        Returns:
            list: List of role names
        """
        try:
            roles_elements = self.find_elements(*self.ROLES_VALUE)
            roles = [elem.text.strip() for elem in roles_elements if elem.text.strip()]
            return roles
        except NoSuchElementException:
            return []

    # ========== Preferences Methods ==========

    def get_language(self) -> Optional[str]:
        """
        Get the language preference value.

        Returns:
            str: Language or None if not found
        """
        return self._get_field_value("Language")

    def get_timezone(self) -> Optional[str]:
        """
        Get the timezone preference value.

        Returns:
            str: Timezone or None if not found
        """
        return self._get_field_value("Time Zone")

    def get_theme(self) -> Optional[str]:
        """
        Get the theme preference value.

        Returns:
            str: Theme or None if not found
        """
        return self._get_field_value("Theme")

    def get_all_preferences(self) -> Dict[str, str]:
        """
        Get all preference fields.

        Returns:
            dict: Preferences with keys: language, timezone, theme
        """
        return {
            'language': self.get_language() or '',
            'timezone': self.get_timezone() or '',
            'theme': self.get_theme() or ''
        }

    # ========== Edit Field Methods ==========

    def _click_edit_button_for_field(self, field_label: str) -> bool:
        """
        Generic method to click edit button for any field using multiple strategies.

        Args:
            field_label: The label of the field (e.g., "Display name", "Email")

        Returns:
            bool: True if button clicked successfully
        """
        try:
            # Strategy 1: Try button in following-sibling td with btn-sm class
            try:
                edit_button = self.driver.find_element(By.XPATH,
                    f"//td[contains(text(), '{field_label}')]/following-sibling::td[1]//button[contains(@class, 'btn-sm')]")
                edit_button.click()
                time.sleep(1)
                return True
            except:
                pass

            # Strategy 2: Try any button in the value cell
            try:
                edit_button = self.driver.find_element(By.XPATH,
                    f"//td[contains(text(), '{field_label}')]/following-sibling::td//button")
                edit_button.click()
                time.sleep(1)
                return True
            except:
                pass

            # Strategy 3: Try button with pencil/edit icon
            try:
                edit_button = self.driver.find_element(By.XPATH,
                    f"//td[contains(text(), '{field_label}')]/following-sibling::td//button[contains(@class, 'bi-pencil') or contains(@class, 'fa-edit') or contains(@class, 'edit')]")
                edit_button.click()
                time.sleep(1)
                return True
            except:
                pass

            # Strategy 4: Try with parent tr approach
            try:
                edit_button = self.driver.find_element(By.XPATH,
                    f"//td[contains(text(), '{field_label}')]/parent::tr//button")
                edit_button.click()
                time.sleep(1)
                return True
            except:
                pass

            return False

        except Exception as e:
            return False

    def click_edit_display_name(self) -> bool:
        """
        Click the edit button for Display Name field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Display name")

    def click_edit_name_jp(self) -> bool:
        """
        Click the edit button for Name (JP) field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Name (JP)")

    def click_edit_name_en(self) -> bool:
        """
        Click the edit button for Name (EN) field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Name (EN)")

    def click_edit_gender(self) -> bool:
        """
        Click the edit button for Gender field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Gender")

    def click_edit_date_of_birth(self) -> bool:
        """
        Click the edit button for Date of Birth field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Date of birth")

    def click_edit_address(self) -> bool:
        """
        Click the edit button for Address field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Address")

    def click_edit_email(self) -> bool:
        """
        Click the edit button for Email field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Email")

    def click_edit_phone(self) -> bool:
        """
        Click the edit button for Phone field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Phone")

    def click_edit_language(self) -> bool:
        """
        Click the edit button for Language field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Language")

    def click_edit_timezone(self) -> bool:
        """
        Click the edit button for Timezone field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Time Zone")

    def click_edit_theme(self) -> bool:
        """
        Click the edit button for Theme field.

        Returns:
            bool: True if button clicked successfully
        """
        return self._click_edit_button_for_field("Theme")

    # ========== Set Field Value Methods ==========

    def _set_input_field_value(self, field_label: str, value: str, locator: tuple, input_type: str = "text") -> bool:
        """
        Generic method to set an input field value using multiple strategies.

        Args:
            field_label: The label of the field (e.g., "Phone", "Email")
            value: The value to set
            locator: Primary CSS/XPath locator tuple
            input_type: Input type attribute if needed (default: "text")

        Returns:
            bool: True if value set successfully
        """
        try:
            # Strategy 1: Try with primary locator
            try:
                wait = WebDriverWait(self.driver, 5)
                input_elem = wait.until(EC.visibility_of_element_located(locator))
                input_elem.clear()
                time.sleep(0.2)
                input_elem.send_keys(value)
                time.sleep(0.3)
                return True
            except:
                pass

            # Strategy 2: Try to find input in the field's row
            try:
                input_elem = self.driver.find_element(By.XPATH,
                    f"//td[contains(text(), '{field_label}')]/following-sibling::td//input")
                input_elem.clear()
                time.sleep(0.2)
                input_elem.send_keys(value)
                time.sleep(0.3)
                return True
            except:
                pass

            # Strategy 3: Try to find input by type if specified
            if input_type != "text":
                try:
                    input_elem = self.driver.find_element(By.CSS_SELECTOR, f"input[type='{input_type}']")
                    input_elem.clear()
                    time.sleep(0.2)
                    input_elem.send_keys(value)
                    time.sleep(0.3)
                    return True
                except:
                    pass

            return False
        except Exception as e:
            return False

    def _set_select_field_value(self, field_label: str, value: str, locator: tuple) -> bool:
        """
        Generic method to set a select field value using multiple strategies.

        Args:
            field_label: The label of the field (e.g., "Language", "Theme")
            value: The option value to select
            locator: Primary CSS/XPath locator tuple

        Returns:
            bool: True if value set successfully
        """
        try:
            # Strategy 1: Try with primary locator
            try:
                wait = WebDriverWait(self.driver, 5)
                select_elem = wait.until(EC.visibility_of_element_located(locator))
                time.sleep(0.5)
                options = select_elem.find_elements(By.TAG_NAME, "option")
                for option in options:
                    if option.text.strip() == value:
                        option.click()
                        time.sleep(0.3)
                        return True
            except:
                pass

            # Strategy 2: Try to find select in the field's row
            try:
                select_elem = self.driver.find_element(By.XPATH,
                    f"//td[contains(text(), '{field_label}')]/following-sibling::td//select")
                time.sleep(0.5)
                options = select_elem.find_elements(By.TAG_NAME, "option")
                for option in options:
                    if option.text.strip() == value:
                        option.click()
                        time.sleep(0.3)
                        return True
            except:
                pass

            return False
        except Exception as e:
            return False

    def set_display_name(self, value: str) -> bool:
        """
        Set the display name value (must call click_edit_display_name first).

        Args:
            value: New display name value

        Returns:
            bool: True if value set successfully
        """
        return self._set_input_field_value("Display name", value, self.DISPLAY_NAME_INPUT)

    def set_name_jp(self, value: str) -> bool:
        """
        Set the Name (JP) value (must call click_edit_name_jp first).

        Args:
            value: New Name (JP) value

        Returns:
            bool: True if value set successfully
        """
        try:
            input_elem = self.wait_until_element_is_clickable(*self.NAME_JP_INPUT)
            input_elem.clear()
            time.sleep(0.2)
            input_elem.send_keys(value)
            time.sleep(0.3)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def set_name_en(self, value: str) -> bool:
        """
        Set the Name (EN) value (must call click_edit_name_en first).

        Args:
            value: New Name (EN) value

        Returns:
            bool: True if value set successfully
        """
        try:
            input_elem = self.wait_until_element_is_clickable(*self.NAME_EN_INPUT)
            input_elem.clear()
            time.sleep(0.2)
            input_elem.send_keys(value)
            time.sleep(0.3)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def set_gender(self, value: str) -> bool:
        """
        Set the gender value (must call click_edit_gender first).

        Args:
            value: Gender value ('Male', 'Female', 'Other')

        Returns:
            bool: True if value set successfully
        """
        try:
            select_elem = self.wait_until_element_is_clickable(*self.GENDER_SELECT)
            # Find and click the option with matching text
            options = select_elem.find_elements(By.TAG_NAME, "option")
            for option in options:
                if option.text.strip() == value:
                    option.click()
                    time.sleep(0.3)
                    return True
            return False
        except (TimeoutException, NoSuchElementException):
            return False

    def set_date_of_birth(self, value: str) -> bool:
        """
        Set the date of birth value (must call click_edit_date_of_birth first).

        Args:
            value: Date value in format 'YYYY-MM-DD'

        Returns:
            bool: True if value set successfully
        """
        try:
            input_elem = self.wait_until_element_is_clickable(*self.DOB_INPUT)
            # Use JavaScript to set the value since it's a date picker
            dob_value = value.replace('-', '/')  # Convert YYYY-MM-DD to YYYY/MM/DD
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                input_elem,
                dob_value
            )
            time.sleep(0.5)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def set_address(self, value: str) -> bool:
        """
        Set the address value (must call click_edit_address first).

        Args:
            value: New address value

        Returns:
            bool: True if value set successfully
        """
        return self._set_input_field_value("Address", value, self.ADDRESS_INPUT)

    def set_email(self, value: str) -> bool:
        """
        Set the email value (must call click_edit_email first).

        Args:
            value: New email value

        Returns:
            bool: True if value set successfully
        """
        return self._set_input_field_value("Email", value, self.EMAIL_INPUT, input_type="email")

    def set_phone(self, value: str) -> bool:
        """
        Set the phone value (must call click_edit_phone first).

        Args:
            value: New phone value

        Returns:
            bool: True if value set successfully
        """
        return self._set_input_field_value("Phone", value, self.PHONE_INPUT, input_type="tel")

    def set_language(self, value: str) -> bool:
        """
        Set the language preference (must call click_edit_language first).

        Args:
            value: Language value (e.g., 'English', 'Japanese')

        Returns:
            bool: True if value set successfully
        """
        return self._set_select_field_value("Language", value, self.LANGUAGE_SELECT)

    def set_timezone(self, value: str) -> bool:
        """
        Set the timezone preference (must call click_edit_timezone first).

        Args:
            value: Timezone value (e.g., 'UTC+9', 'UTC+7')

        Returns:
            bool: True if value set successfully
        """
        return self._set_select_field_value("Time Zone", value, self.TIMEZONE_SELECT)

    def set_theme(self, value: str) -> bool:
        """
        Set the theme preference (must call click_edit_theme first).

        Args:
            value: Theme value (e.g., 'Light', 'Dark')

        Returns:
            bool: True if value set successfully
        """
        return self._set_select_field_value("Theme", value, self.THEME_SELECT)

    # ========== Save/Cancel Methods ==========

    def click_save_button(self) -> bool:
        """
        Click the Save button to save profile changes.

        Note: The save button appears after editing a field and contains an SVG checkmark icon.
        It has aria-label="Save" and classes "btn btn-link btn-sm btn-square".
        The button starts disabled and becomes enabled after valid input.

        Returns:
            bool: True if button clicked successfully
        """
        try:
            # Strategy 1: Try with aria-label="Save" - wait for it to become enabled
            try:
                # First wait for the button to appear
                wait = WebDriverWait(self.driver, 10)
                save_button = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//button[@aria-label='Save']")))

                # Then wait for it to become enabled (disabled attribute removed)
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='Save' and not(@disabled)]")))

                # Add small delay to ensure button is fully ready
                time.sleep(0.5)
                save_button.click()
                time.sleep(3)  # Wait longer for save operation to complete
                return True
            except:
                pass

            # Strategy 2: Try finding button with checkmark SVG icon
            try:
                wait = WebDriverWait(self.driver, 5)
                # Wait for button to be present first
                save_button = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(@class, 'btn-square')]//svg[contains(@class, 'iconsvg-check')]/..")))

                # Wait for it to be clickable (not disabled)
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'btn-square') and not(@disabled)]//svg[contains(@class, 'iconsvg-check')]/..")))

                time.sleep(0.5)
                save_button.click()
                time.sleep(3)
                return True
            except:
                pass

            # Strategy 3: Try finding first enabled btn-square button
            try:
                wait = WebDriverWait(self.driver, 10)
                save_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'btn-square') and not(@disabled)]")))
                time.sleep(0.5)
                save_button.click()
                time.sleep(3)
                return True
            except:
                pass

            # Strategy 4: Original locator for backwards compatibility
            try:
                save_button = self.wait_until_element_is_clickable(*self.SAVE_BUTTON)
                save_button.click()
                time.sleep(3)
                return True
            except:
                pass

            return False
        except Exception as e:
            return False

    def click_cancel_button(self) -> bool:
        """
        Click the Cancel button to discard profile changes.

        Note: The cancel button appears after editing a field, similar to save button.
        It likely has aria-label="Cancel" and contains an X icon.

        Returns:
            bool: True if button clicked successfully
        """
        try:
            # Strategy 1: Try with aria-label="Cancel"
            try:
                wait = WebDriverWait(self.driver, 10)
                cancel_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[@aria-label='Cancel' and not(@disabled)]")))
                cancel_button.click()
                time.sleep(1)
                return True
            except:
                pass

            # Strategy 2: Try finding button with X icon
            try:
                cancel_button = self.driver.find_element(By.XPATH,
                    "//button[contains(@class, 'btn-square')]//svg[contains(@class, 'iconsvg-x') or contains(@class, 'iconsvg-close')]/..")
                cancel_button.click()
                time.sleep(1)
                return True
            except:
                pass

            # Strategy 3: Try finding second btn-square button (assuming save is first, cancel is second)
            try:
                buttons = self.driver.find_elements(By.XPATH,
                    "//button[contains(@class, 'btn-square') and not(@disabled)]")
                if len(buttons) >= 2:
                    buttons[1].click()  # Second button is usually cancel
                    time.sleep(1)
                    return True
            except:
                pass

            # Strategy 4: Original locator
            try:
                cancel_button = self.wait_until_element_is_clickable(*self.CANCEL_BUTTON)
                cancel_button.click()
                time.sleep(1)
                return True
            except:
                pass

            return False
        except Exception as e:
            return False

    # ========== Change Password Modal Methods ==========

    def open_change_password_modal(self) -> bool:
        """
        Open the Change Password modal dialog.

        Returns:
            bool: True if modal opened successfully
        """
        try:
            change_password_button = self.wait_until_element_is_clickable(*self.CHANGE_PASSWORD_BUTTON)
            change_password_button.click()

            # Wait for modal to appear
            self.wait.until(EC.visibility_of_element_located(self.CHANGE_PASSWORD_MODAL))
            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def fill_change_password_form(self, current_password: str, new_password: str, confirm_password: str) -> bool:
        """
        Fill out the Change Password form with provided data.

        Args:
            current_password: Current password
            new_password: New password
            confirm_password: Confirmation of new password

        Returns:
            bool: True if form filled successfully
        """
        try:
            # Current Password
            current_pwd_input = self.wait_until_element_is_clickable(*self.CURRENT_PASSWORD_INPUT)
            current_pwd_input.clear()
            current_pwd_input.send_keys(current_password)
            time.sleep(0.3)

            # New Password
            new_pwd_input = self.wait_until_element_is_clickable(*self.NEW_PASSWORD_INPUT)
            new_pwd_input.clear()
            new_pwd_input.send_keys(new_password)
            time.sleep(0.3)

            # Confirm Password
            confirm_pwd_input = self.wait_until_element_is_clickable(*self.CONFIRM_PASSWORD_INPUT)
            confirm_pwd_input.clear()
            confirm_pwd_input.send_keys(confirm_password)
            time.sleep(0.3)

            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def submit_change_password(self) -> bool:
        """
        Submit the Change Password form by clicking the submit button.

        Returns:
            bool: True if submission successful
        """
        try:
            submit_button = self.wait_until_element_is_clickable(*self.CHANGE_PASSWORD_SUBMIT_BUTTON)
            submit_button.click()

            # Wait for modal to close
            time.sleep(3)

            # Check if modal is closed
            try:
                modal = self.driver.find_element(*self.CHANGE_PASSWORD_MODAL)
                is_displayed = modal.is_displayed()
                return not is_displayed  # Return True if modal is no longer displayed
            except NoSuchElementException:
                return True  # Modal not found means it's closed

        except (TimeoutException, NoSuchElementException):
            return False

    def cancel_change_password(self) -> bool:
        """
        Cancel the Change Password form by clicking the cancel button.

        Returns:
            bool: True if cancellation successful
        """
        try:
            cancel_button = self.wait_until_element_is_clickable(*self.CHANGE_PASSWORD_CANCEL_BUTTON)
            cancel_button.click()

            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False

    def close_change_password_modal(self) -> bool:
        """
        Close the Change Password modal using the X button.

        Returns:
            bool: True if modal closed successfully
        """
        try:
            close_button = self.wait_until_element_is_clickable(*self.CHANGE_PASSWORD_CLOSE_BUTTON)
            close_button.click()

            time.sleep(1)
            return True

        except (TimeoutException, NoSuchElementException):
            return False
