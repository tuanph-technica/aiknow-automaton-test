"""
Documents Page Object Module

This module provides a comprehensive page object for the Documents management page,
including file upload, search, filtering, and document list management functionality.
"""

import os
import time
from typing import List, Optional, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from base.base_driver import BaseDriver


class Documents(BaseDriver):
    """
    Page Object for Documents management page.

    Inherits from BaseDriver to provide Selenium WebDriver utilities
    and custom waiting/interaction methods.
    """

    # Locators - Upload Zone
    UPLOAD_ZONE = (By.TAG_NAME, "app-document-upload-zone")
    FILE_INPUT = (By.CSS_SELECTOR, "input[type='file'][accept*='.pdf']")
    UPLOAD_AREA = (By.CSS_SELECTOR, ".upload-area")

    # Locators - Search and Filters
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Search by file name']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".btn-primary.filter-btn")
    RESET_BUTTON = (By.CSS_SELECTOR, ".btn-outline-gray.filter-btn")

    # Filter Dropdowns
    CREATED_BY_SELECT = (By.CSS_SELECTOR, "select.form-select.choices__input[appusersearchable]")
    UPLOAD_STATUS_SELECT = (By.XPATH, "//select[@data-plugin='choices'][.//option[@value='UPLOADING']]")
    EXTRACT_STATUS_SELECT = (By.XPATH, "//select[@data-plugin='choices'][.//option[@value='NOT_REQUESTED']]")
    DATE_RANGE_INPUT = (By.CSS_SELECTOR, ".flatpickr-range input[data-input]")

    # Locators - Document List
    DELETE_ALL_BUTTON = (By.CSS_SELECTOR, ".btn-outline-danger")
    DOCUMENT_TABLE = (By.CSS_SELECTOR, ".table-document")
    TABLE_ROWS = (By.CSS_SELECTOR, ".table-document tbody tr")
    TABLE_HEADER = (By.CSS_SELECTOR, ".table-document thead tr")

    # Column indices (0-based)
    COL_FILENAME = 0
    COL_TYPE = 1
    COL_SIZE = 2
    COL_UPLOAD_STATUS = 3
    COL_EXTRACT_STATUS = 4
    COL_EXTRACT_TIME = 5
    COL_CREATED_DATE = 6
    COL_CREATED_BY = 7
    COL_ACTION = 8

    # Locators - Pagination
    PAGINATOR = (By.CSS_SELECTOR, "mat-paginator")
    PAGINATION_RANGE = (By.CSS_SELECTOR, ".mat-mdc-paginator-range-label")
    NEXT_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-next")
    PREV_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-previous")
    FIRST_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-first")
    LAST_PAGE_BUTTON = (By.CSS_SELECTOR, ".mat-mdc-paginator-navigation-last")
    PAGE_SIZE_SELECT = (By.CSS_SELECTOR, ".mat-mdc-paginator-page-size-select mat-select")

    # Locators - Confirmation Modal
    CONFIRM_MODAL = (By.ID, "modal-document-delete-confirm")
    CONFIRM_CANCEL_BUTTON = (By.CSS_SELECTOR, "#modal-document-delete-confirm .btn-outline-gray")
    CONFIRM_OK_BUTTON = (By.CSS_SELECTOR, "#modal-document-delete-confirm .btn-primary")

    # Status values
    UPLOAD_STATUS_UPLOADING = "UPLOADING"
    UPLOAD_STATUS_UPLOADED = "UPLOADED"
    UPLOAD_STATUS_VIRUS_SCANNING = "VIRUS_SCANNING"
    UPLOAD_STATUS_FAILED = "FAILED_UPLOAD"

    EXTRACT_STATUS_NOT_REQUESTED = "NOT_REQUESTED"
    EXTRACT_STATUS_EXTRACTING = "EXTRACTING"
    EXTRACT_STATUS_EXTRACTED = "EXTRACTED"
    EXTRACT_STATUS_FAILED = "FAILED_EXTRACT"

    def __init__(self, driver):
        """
        Initialize Documents page object.

        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    # ========== Upload Methods ==========

    def upload_file(self, file_path: str, category_name: str = "Report") -> bool:
        """
        Upload a file using the file input element. Upload happens automatically.

        Args:
            file_path: Path to the file to upload (can be relative or absolute)
            category_name: Category to assign to the document (default: "Report")

        Returns:
            bool: True if upload completed successfully, False otherwise
        """
        try:
            # Convert to absolute path
            absolute_path = os.path.abspath(file_path)

            if not os.path.exists(absolute_path):
                print(f"File not found: {absolute_path}")
                return False

            # Locate the file input (it's hidden, so we interact directly)
            file_input = self.wait.until(
                EC.presence_of_element_located(self.FILE_INPUT)
            )

            # Send the file path to the input element
            file_input.send_keys(absolute_path)

            filename = os.path.basename(absolute_path)
            print(f"File selected: {filename}")

            # Wait for file to appear in upload table with "Uploaded" status
            time.sleep(2)

            # Wait for upload to complete - look for the uploaded file in table
            max_wait = 10
            for i in range(max_wait):
                try:
                    upload_zone = self.driver.find_element(*self.UPLOAD_ZONE)
                    upload_table = upload_zone.find_element(By.CSS_SELECTOR, "table.table-upload-document")
                    rows = upload_table.find_elements(By.TAG_NAME, "tr")

                    for row in rows:
                        tds = row.find_elements(By.TAG_NAME, "td")
                        if len(tds) >= 4:
                            file_name_td = tds[0].text.strip()
                            status_td = tds[3].text.strip()

                            if filename in file_name_td and status_td == "Uploaded":
                                print(f"File uploaded successfully: {filename}")

                                # Click the "Upload file" button to confirm
                                try:
                                    upload_btn = upload_table.find_element(By.CSS_SELECTOR, "button.btn-primary")
                                    upload_btn.click()
                                    print("Clicked Upload file button")
                                    time.sleep(2)
                                except:
                                    print("No Upload file button found or already confirmed")

                                return True
                except:
                    pass

                time.sleep(1)

            print(f"Upload verification timeout for: {filename}")
            return False

        except Exception as e:
            print(f"Failed to upload file: {e}")
            import traceback
            traceback.print_exc()
            return False

    def process_upload_file(self, category_name: str = "Report") -> bool:
        """
        Process the upload by selecting category and clicking upload button.

        Args:
            category_name: Category to assign to the document

        Returns:
            bool: True if processing successful, False otherwise
        """
        try:
            # Wait for upload zone to be ready
            upload_div = self.wait.until(
                EC.presence_of_element_located(self.UPLOAD_ZONE)
            )

            # Click the link to show category selection
            try:
                a_link = upload_div.find_element(By.TAG_NAME, "a")
                a_link.click()
                time.sleep(1)
            except:
                print("No link to click, category selection might already be visible")

            # Find and select category dropdown
            dropdowns = upload_div.find_elements(By.TAG_NAME, "select")
            if len(dropdowns) > 0:
                time.sleep(1)
                dropdowns[0].click()
                time.sleep(0.5)

                # Find and select the category option
                options = dropdowns[0].find_elements(By.TAG_NAME, "option")
                category_found = False
                for option in options:
                    if option.text.strip() == category_name:
                        option.click()
                        category_found = True
                        print(f"Selected category: {category_name}")
                        break

                if not category_found:
                    print(f"Category '{category_name}' not found, using first option")
                    if len(options) > 0:
                        options[0].click()

                time.sleep(0.5)

            # Click the upload/confirm button
            button = upload_div.find_element(By.TAG_NAME, "button")
            button.click()
            time.sleep(1)

            print("Upload processing completed")
            return True

        except Exception as e:
            print(f"Failed to process upload: {e}")
            return False

    def upload_multiple_files(self, file_paths: List[str]) -> bool:
        """
        Upload multiple files at once.

        Args:
            file_paths: List of file paths to upload

        Returns:
            bool: True if all uploads initiated successfully, False otherwise
        """
        try:
            # Convert all paths to absolute
            absolute_paths = [os.path.abspath(fp) for fp in file_paths]

            # Verify all files exist
            for path in absolute_paths:
                if not os.path.exists(path):
                    print(f"File not found: {path}")
                    return False

            # Locate the file input
            file_input = self.wait.until(
                EC.presence_of_element_located(self.FILE_INPUT)
            )

            # Join paths with newline for multiple file upload
            combined_paths = "\n".join(absolute_paths)
            file_input.send_keys(combined_paths)
            time.sleep(2)  # Wait for uploads to initiate

            print(f"Successfully uploaded {len(absolute_paths)} files")
            return True

        except Exception as e:
            print(f"Failed to upload multiple files: {e}")
            return False

    def is_upload_area_visible(self) -> bool:
        """Check if upload area is visible."""
        try:
            upload_area = self.find_element(*self.UPLOAD_AREA)
            return upload_area.is_displayed()
        except:
            return False

    # ========== Search and Filter Methods ==========

    def search_by_filename(self, filename: str) -> bool:
        """
        Search for documents by filename.

        Args:
            filename: Filename or partial filename to search for

        Returns:
            bool: True if search executed successfully, False otherwise
        """
        try:
            # Clear and enter search text
            search_input = self.wait.until(
                EC.presence_of_element_located(self.SEARCH_INPUT)
            )
            search_input.clear()
            search_input.send_keys(filename)
            time.sleep(0.5)

            # Click search button
            search_btn = self.find_element(*self.SEARCH_BUTTON)
            search_btn.click()
            time.sleep(1)  # Wait for results to load

            print(f"Searched for filename: {filename}")
            return True

        except Exception as e:
            print(f"Failed to search by filename: {e}")
            return False

    def filter_by_upload_status(self, status: str) -> bool:
        """
        Filter documents by upload status.

        Args:
            status: Upload status value (UPLOADING, UPLOADED, VIRUS_SCANNING, FAILED_UPLOAD)

        Returns:
            bool: True if filter applied successfully, False otherwise
        """
        try:
            # Click on the upload status dropdown
            select_element = self.find_element(*self.UPLOAD_STATUS_SELECT)

            # Find the parent choices div and click to open dropdown
            choices_div = select_element.find_element(By.XPATH, "./ancestor::div[@class='choices']")
            choices_div.click()
            time.sleep(0.5)

            # Click the option with matching value
            option_xpath = f"//div[@data-value='{status}'][@role='option']"
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, option_xpath))
            )
            option.click()
            time.sleep(1)

            print(f"Filtered by upload status: {status}")
            return True

        except Exception as e:
            print(f"Failed to filter by upload status: {e}")
            return False

    def filter_by_extract_status(self, status: str) -> bool:
        """
        Filter documents by extract status.

        Args:
            status: Extract status value (NOT_REQUESTED, EXTRACTING, EXTRACTED, FAILED_EXTRACT)

        Returns:
            bool: True if filter applied successfully, False otherwise
        """
        try:
            # Click on the extract status dropdown
            select_element = self.find_element(*self.EXTRACT_STATUS_SELECT)

            # Find the parent choices div and click to open dropdown
            choices_div = select_element.find_element(By.XPATH, "./ancestor::div[@class='choices']")
            choices_div.click()
            time.sleep(0.5)

            # Click the option with matching value
            option_xpath = f"//div[@data-value='{status}'][@role='option']"
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, option_xpath))
            )
            option.click()
            time.sleep(1)

            print(f"Filtered by extract status: {status}")
            return True

        except Exception as e:
            print(f"Failed to filter by extract status: {e}")
            return False

    def reset_filters(self) -> bool:
        """
        Reset all filters to default.

        Returns:
            bool: True if reset successful, False otherwise
        """
        try:
            reset_btn = self.find_element(*self.RESET_BUTTON)
            reset_btn.click()
            time.sleep(1)

            print("Filters reset successfully")
            return True

        except Exception as e:
            print(f"Failed to reset filters: {e}")
            return False

    # ========== Document List Methods ==========

    def get_document_count(self) -> int:
        """
        Get the total number of documents in the current view.

        Returns:
            int: Number of document rows visible
        """
        try:
            rows = self.find_elements(*self.TABLE_ROWS)
            return len(rows)
        except:
            return 0

    def get_document_row(self, row_index: int) -> Optional[WebElement]:
        """
        Get a specific document row by index.

        Args:
            row_index: 0-based row index

        Returns:
            WebElement or None: The row element if found
        """
        try:
            rows = self.find_elements(*self.TABLE_ROWS)
            if 0 <= row_index < len(rows):
                return rows[row_index]
            return None
        except:
            return None

    def get_document_info(self, row_index: int) -> Optional[dict]:
        """
        Get document information from a specific row.

        Args:
            row_index: 0-based row index

        Returns:
            dict or None: Document information dictionary
        """
        try:
            row = self.get_document_row(row_index)
            if not row:
                return None

            cells = row.find_elements(By.TAG_NAME, "td")

            return {
                'filename': cells[self.COL_FILENAME].text.strip(),
                'type': cells[self.COL_TYPE].text.strip(),
                'size': cells[self.COL_SIZE].text.strip(),
                'upload_status': cells[self.COL_UPLOAD_STATUS].text.strip(),
                'extract_status': cells[self.COL_EXTRACT_STATUS].text.strip(),
                'extract_time': cells[self.COL_EXTRACT_TIME].text.strip(),
                'created_date': cells[self.COL_CREATED_DATE].text.strip(),
                'created_by': cells[self.COL_CREATED_BY].text.strip()
            }

        except Exception as e:
            print(f"Failed to get document info: {e}")
            return None

    def find_document_by_name(self, filename: str) -> Tuple[Optional[int], Optional[dict]]:
        """
        Find a document by filename in the current page.

        Args:
            filename: Filename to search for (exact or partial match)

        Returns:
            tuple: (row_index, document_info) or (None, None) if not found
        """
        try:
            count = self.get_document_count()
            for i in range(count):
                doc_info = self.get_document_info(i)
                if doc_info and filename in doc_info['filename']:
                    return (i, doc_info)
            return (None, None)

        except Exception as e:
            print(f"Failed to find document: {e}")
            return (None, None)

    def get_all_documents(self) -> List[dict]:
        """
        Get information for all documents in the current page.

        Returns:
            list: List of document information dictionaries
        """
        documents = []
        count = self.get_document_count()

        for i in range(count):
            doc_info = self.get_document_info(i)
            if doc_info:
                documents.append(doc_info)

        return documents

    # ========== Delete Methods ==========

    def delete_document_by_index(self, row_index: int, confirm: bool = True) -> bool:
        """
        Delete a document by row index.

        Args:
            row_index: 0-based row index
            confirm: Whether to confirm the deletion (default: True)

        Returns:
            bool: True if deletion initiated successfully, False otherwise
        """
        try:
            row = self.get_document_row(row_index)
            if not row:
                print(f"Row {row_index} not found")
                return False

            # Find and click the delete button in the action column
            delete_btn = row.find_element(By.CSS_SELECTOR, "button svg.iconsvg-trash")
            delete_btn.find_element(By.XPATH, "./..").click()  # Click parent button
            time.sleep(0.5)

            # Handle confirmation modal if it appears
            if confirm:
                return self.confirm_deletion()

            return True

        except Exception as e:
            print(f"Failed to delete document at row {row_index}: {e}")
            return False

    def delete_document_by_name(self, filename: str, confirm: bool = True) -> bool:
        """
        Delete a document by filename.

        Args:
            filename: Filename to delete
            confirm: Whether to confirm the deletion (default: True)

        Returns:
            bool: True if deletion initiated successfully, False otherwise
        """
        try:
            row_index, _ = self.find_document_by_name(filename)
            if row_index is None:
                print(f"Document not found: {filename}")
                return False

            return self.delete_document_by_index(row_index, confirm)

        except Exception as e:
            print(f"Failed to delete document '{filename}': {e}")
            return False

    def delete_all_documents(self, confirm: bool = True) -> bool:
        """
        Delete all documents using the "Delete all files" button.

        Args:
            confirm: Whether to confirm the deletion (default: True)

        Returns:
            bool: True if deletion initiated successfully, False otherwise
        """
        try:
            delete_all_btn = self.wait.until(
                EC.element_to_be_clickable(self.DELETE_ALL_BUTTON)
            )
            delete_all_btn.click()
            time.sleep(0.5)

            # Handle confirmation modal if it appears
            if confirm:
                return self.confirm_deletion()

            return True

        except Exception as e:
            print(f"Failed to delete all documents: {e}")
            return False

    def confirm_deletion(self) -> bool:
        """
        Confirm a deletion in the confirmation modal.

        Returns:
            bool: True if confirmation successful, False otherwise
        """
        try:
            confirm_btn = self.wait.until(
                EC.element_to_be_clickable(self.CONFIRM_OK_BUTTON)
            )
            confirm_btn.click()
            time.sleep(1)

            print("Deletion confirmed")
            return True

        except TimeoutException:
            # Modal might not appear for some operations
            print("No confirmation modal found")
            return True
        except Exception as e:
            print(f"Failed to confirm deletion: {e}")
            return False

    def cancel_deletion(self) -> bool:
        """
        Cancel a deletion in the confirmation modal.

        Returns:
            bool: True if cancellation successful, False otherwise
        """
        try:
            cancel_btn = self.wait.until(
                EC.element_to_be_clickable(self.CONFIRM_CANCEL_BUTTON)
            )
            cancel_btn.click()
            time.sleep(0.5)

            print("Deletion cancelled")
            return True

        except Exception as e:
            print(f"Failed to cancel deletion: {e}")
            return False

    # ========== Pagination Methods ==========

    def get_pagination_info(self) -> Optional[dict]:
        """
        Get pagination information (current range and total).

        Returns:
            dict or None: {'start': int, 'end': int, 'total': int} or None
        """
        try:
            range_label = self.find_element(*self.PAGINATION_RANGE)
            text = range_label.text  # e.g., "1-10 of 83 results."

            # Parse the text
            parts = text.split()
            range_part = parts[0]  # "1-10"
            total_part = parts[2]  # "83"

            start, end = map(int, range_part.split('-'))
            total = int(total_part)

            return {
                'start': start,
                'end': end,
                'total': total
            }

        except Exception as e:
            print(f"Failed to get pagination info: {e}")
            return None

    def go_to_next_page(self) -> bool:
        """Navigate to the next page."""
        try:
            next_btn = self.find_element(*self.NEXT_PAGE_BUTTON)
            if 'mat-mdc-button-disabled' in next_btn.get_attribute('class'):
                print("Already on last page")
                return False

            next_btn.click()
            time.sleep(1)
            return True

        except Exception as e:
            print(f"Failed to go to next page: {e}")
            return False

    def go_to_previous_page(self) -> bool:
        """Navigate to the previous page."""
        try:
            prev_btn = self.find_element(*self.PREV_PAGE_BUTTON)
            if 'mat-mdc-button-disabled' in prev_btn.get_attribute('class'):
                print("Already on first page")
                return False

            prev_btn.click()
            time.sleep(1)
            return True

        except Exception as e:
            print(f"Failed to go to previous page: {e}")
            return False

    def go_to_first_page(self) -> bool:
        """Navigate to the first page."""
        try:
            first_btn = self.find_element(*self.FIRST_PAGE_BUTTON)
            first_btn.click()
            time.sleep(1)
            return True

        except Exception as e:
            print(f"Failed to go to first page: {e}")
            return False

    def go_to_last_page(self) -> bool:
        """Navigate to the last page."""
        try:
            last_btn = self.find_element(*self.LAST_PAGE_BUTTON)
            last_btn.click()
            time.sleep(1)
            return True

        except Exception as e:
            print(f"Failed to go to last page: {e}")
            return False

    # ========== Verification Methods ==========

    def is_document_present(self, filename: str) -> bool:
        """
        Check if a document with the given filename is present.

        Args:
            filename: Filename to check

        Returns:
            bool: True if document found, False otherwise
        """
        row_index, _ = self.find_document_by_name(filename)
        return row_index is not None

    def verify_upload_status(self, filename: str, expected_status: str) -> bool:
        """
        Verify the upload status of a document.

        Args:
            filename: Document filename
            expected_status: Expected upload status

        Returns:
            bool: True if status matches, False otherwise
        """
        _, doc_info = self.find_document_by_name(filename)
        if doc_info:
            return doc_info['upload_status'] == expected_status
        return False

    def verify_extract_status(self, filename: str, expected_status: str) -> bool:
        """
        Verify the extract status of a document.

        Args:
            filename: Document filename
            expected_status: Expected extract status

        Returns:
            bool: True if status matches, False otherwise
        """
        _, doc_info = self.find_document_by_name(filename)
        if doc_info:
            return doc_info['extract_status'] == expected_status
        return False

    def wait_for_upload_complete(self, filename: str, timeout: int = 30) -> bool:
        """
        Wait for a document upload to complete.

        Args:
            filename: Document filename to wait for
            timeout: Maximum wait time in seconds

        Returns:
            bool: True if upload completed, False if timeout
        """
        end_time = time.time() + timeout

        while time.time() < end_time:
            if self.verify_upload_status(filename, self.UPLOAD_STATUS_UPLOADED):
                print(f"Upload completed for: {filename}")
                return True
            time.sleep(2)

        print(f"Upload timeout for: {filename}")
        return False

    def wait_for_extraction_complete(self, filename: str, timeout: int = 60) -> bool:
        """
        Wait for a document extraction to complete.

        Args:
            filename: Document filename to wait for
            timeout: Maximum wait time in seconds

        Returns:
            bool: True if extraction completed, False if timeout
        """
        end_time = time.time() + timeout

        while time.time() < end_time:
            if self.verify_extract_status(filename, self.EXTRACT_STATUS_EXTRACTED):
                print(f"Extraction completed for: {filename}")
                return True
            time.sleep(2)

        print(f"Extraction timeout for: {filename}")
        return False
