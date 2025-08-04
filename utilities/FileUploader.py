import time
import pyautogui
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class FileUploader:
    """
    A comprehensive file uploader class using Selenium and PyAutoGUI
    Supports single file, multiple files, and random file selection
    """

    def __init__(self, driver=None, headless=False, implicit_wait=10, base_dir=None):
        """
        Initialize FileUploader

        Args:
            driver: Existing WebDriver instance (optional)
            headless: Run browser in headless mode
            implicit_wait: Implicit wait time for elements
            base_dir: Base directory for relative paths (optional)
        """
        self.driver = driver
        self.headless = headless
        self.implicit_wait = implicit_wait
        self.should_quit_driver = False
        self.base_dir = base_dir or os.getcwd()  # Use current directory if not specified

        if not self.driver:
            self._setup_driver()
            self.should_quit_driver = True

    def _setup_driver(self):
        """Setup Chrome WebDriver with options"""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(self.implicit_wait)

    def handle_file_dialog(self, file_path):
        """
        Handle Windows file dialog using pyautogui for single file

        Args:
            file_path: Path to the file to select
        """
        time.sleep(2)  # Wait for dialog to open

        # Type the file path
        pyautogui.write(file_path)
        pyautogui.press('enter')

        time.sleep(1)  # Wait for file to be selected

    def handle_multiple_files_dialog(self, file_paths):
        """
        Handle Windows file dialog for multiple files using pyautogui

        Args:
            file_paths: List of file paths to select
        """
        time.sleep(2)  # Wait for dialog to open

        # Navigate to the directory of the first file
        first_file_dir = os.path.dirname(file_paths[0])
        pyautogui.write(first_file_dir)
        pyautogui.press('enter')
        time.sleep(1)

        # Select multiple files
        for i, file_path in enumerate(file_paths):
            file_name = os.path.basename(file_path)

            if i == 0:
                # First file - just type filename
                i = 1
                pyautogui.write(file_name)
            else:
                # Hold Ctrl and select additional files
                pyautogui.keyDown('ctrl')
                time.sleep(0.1)
                pyautogui.write(file_name)
                pyautogui.press('enter')
                pyautogui.keyUp('ctrl')

            time.sleep(0.5)  # Small delay between selections

        # Confirm selection
        pyautogui.press('enter')
        time.sleep(1)

    def resolve_file_path(self, file_path):
        """
        Resolve relative file paths to absolute paths

        Args:
            file_path: Relative or absolute file path

        Returns:
            Absolute file path
        """
        if os.path.isabs(file_path):
            return file_path
        else:
            return os.path.join(self.base_dir, file_path)

    def scan_directory(self, directory=None, extensions=None, recursive=True):
        """
        Scan directory for files with specific extensions

        Args:
            directory: Directory to scan (uses base_dir if None)
            extensions: List of file extensions to include (e.g., ['.pdf', '.jpg'])
            recursive: Scan subdirectories recursively

        Returns:
            List of file paths
        """
        scan_dir = directory or self.base_dir

        if not os.path.exists(scan_dir):
            print(f"Directory not found: {scan_dir}")
            return []

        files = []

        if recursive:
            for root, dirs, filenames in os.walk(scan_dir):
                for filename in filenames:
                    if not extensions or any(filename.lower().endswith(ext.lower()) for ext in extensions):
                        files.append(os.path.join(root, filename))
        else:
            for filename in os.listdir(scan_dir):
                file_path = os.path.join(scan_dir, filename)
                if os.path.isfile(file_path):
                    if not extensions or any(filename.lower().endswith(ext.lower()) for ext in extensions):
                        files.append(file_path)

        print(f"Found {len(files)} files in {scan_dir}")
        for i, file_path in enumerate(files[:10], 1):  # Show first 10 files
            print(f"  {i}. {os.path.basename(file_path)}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more files")

        return files
        """
        Select m random files from n files

        Args:
            file_list: List of file paths
            m: Number of files to select

        Returns:
            List of randomly selected file paths
        """
        if m > len(file_list):
            print(f"Warning: Requested {m} files but only {len(file_list)} available")
            m = len(file_list)

        # Filter existing files
        existing_files = [f for f in file_list if os.path.exists(f)]

        if not existing_files:
            print("No existing files found")
            return []

        if m > len(existing_files):
            print(f"Warning: Only {len(existing_files)} files exist")
            m = len(existing_files)

        selected = random.sample(existing_files, m)
        print(f"Randomly selected {len(selected)} files:")
        for i, file_path in enumerate(selected, 1):
            print(f"  {i}. {os.path.basename(file_path)}")

        return selected

    def filter_files(self, file_list, file_types=None, min_size=None, max_size=None):
        """
        Filter files based on criteria

        Args:
            file_list: List of file paths (can be relative or absolute)
            file_types: List of allowed extensions (e.g., ['.pdf', '.jpg'])
            min_size: Minimum file size in bytes
            max_size: Maximum file size in bytes

        Returns:
            List of filtered absolute file paths
        """
        filtered_files = []

        for file_path in file_list:
            # Convert to absolute path
            abs_path = self.resolve_file_path(file_path)

            if not os.path.exists(abs_path):
                continue

            # Check file type
            if file_types:
                file_ext = os.path.splitext(abs_path)[1].lower()
                if file_ext not in [ext.lower() for ext in file_types]:
                    continue

            # Check file size
            try:
                file_size = os.path.getsize(abs_path)
                if min_size and file_size < min_size:
                    continue
                if max_size and file_size > max_size:
                    continue
            except OSError:
                continue

            filtered_files.append(abs_path)

        print(f"Filtered {len(filtered_files)} files from {len(file_list)} total files")
        return filtered_files

    def upload_single_file(self, upload_button_selector, file_path, website_url=None):
        """
        Upload a single file

        Args:
            upload_button_selector: CSS selector for upload button
            file_path: Path to the file to upload (can be relative or absolute)
            website_url: URL to navigate to (optional)

        Returns:
            bool: Success status
        """
        try:
            if website_url:
                self.driver.get(website_url)
                time.sleep(3)

            # Convert to absolute path
            abs_file_path = self.resolve_file_path(file_path)

            if not os.path.exists(abs_file_path):
                print(f"File not found: {abs_file_path}")
                return False

            print(f"Uploading file: {os.path.basename(abs_file_path)}")

            # Wait for upload button and click
            upload_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, upload_button_selector))
            )
            upload_button.click()

            # Handle file dialog
            self.handle_file_dialog(abs_file_path)

            print("File upload completed successfully!")
            return True

        except Exception as e:
            print(f"Error uploading single file: {e}")
            return False

    def upload_multiple_files(self, upload_button_selector, file_paths, website_url=None):
        """
        Upload multiple files at once

        Args:
            upload_button_selector: CSS selector for upload button (should support multiple)
            file_paths: List of file paths to upload
            website_url: URL to navigate to (optional)

        Returns:
            bool: Success status
        """
        try:
            if website_url:
                self.driver.get(website_url)
                time.sleep(3)

            # Validate files
            valid_files = [f for f in file_paths if os.path.exists(f)]

            if not valid_files:
                print("No valid files to upload")
                return False

            print(f"Uploading {len(valid_files)} files simultaneously:")
            for i, file_path in enumerate(valid_files, 1):
                print(f"  {i}. {os.path.basename(file_path)}")

            # Wait for upload button and click
            upload_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, upload_button_selector))
            )
            upload_button.click()

            # Handle multiple files dialog
            self.handle_multiple_files_dialog(valid_files)

            print("Multiple files upload completed successfully!")
            return True

        except Exception as e:
            print(f"Error uploading multiple files: {e}")
            return False

    def upload_files_sequentially(self, upload_button_selector, file_paths,
                                  website_url=None, delay=2):
        """
        Upload files one by one (for sites that don't support multiple selection)

        Args:
            upload_button_selector: CSS selector for upload button
            file_paths: List of file paths to upload
            website_url: URL to navigate to (optional)
            delay: Delay between uploads in seconds

        Returns:
            bool: Success status
        """
        try:
            if website_url:
                self.driver.get(website_url)
                time.sleep(3)

            valid_files = [f for f in file_paths if os.path.exists(f)]

            if not valid_files:
                print("No valid files to upload")
                return False

            success_count = 0

            for i, file_path in enumerate(valid_files, 1):
                try:
                    print(f"Uploading file {i}/{len(valid_files)}: {os.path.basename(file_path)}")

                    # Wait for upload button and click
                    upload_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, upload_button_selector))
                    )
                    upload_button.click()

                    # Handle single file dialog
                    self.handle_file_dialog(file_path)

                    success_count += 1

                    # Wait between uploads
                    if i < len(valid_files):
                        time.sleep(delay)

                except Exception as e:
                    print(f"Error uploading {os.path.basename(file_path)}: {e}")

            print(f"Sequential upload completed: {success_count}/{len(valid_files)} files")
            return success_count > 0

        except Exception as e:
            print(f"Error in sequential upload: {e}")
            return False

    def upload_random_files(self, upload_button_selector, file_list, m, website_url=None,
                            sequential=False, delay=2, **filter_kwargs):
        """
        Upload m random files from n available files with optional filtering

        Args:
            upload_button_selector: CSS selector for upload button
            file_list: List of all available file paths (n files)
            m: Number of files to randomly select and upload
            website_url: URL to navigate to (optional)
            sequential: If True, upload files one by one
            delay: Delay between sequential uploads
            **filter_kwargs: Additional filtering options (file_types, min_size, max_size)

        Returns:
            bool: Success status
        """
        try:
            if website_url:
                self.driver.get(website_url)
                time.sleep(3)

            # Apply filters if provided
            if filter_kwargs:
                filtered_files = self.filter_files(file_list, **filter_kwargs)
            else:
                filtered_files = file_list

            # Select random files
            selected_files = self.select_random_files(filtered_files, m)

            if not selected_files:
                print("No files selected for upload")
                return False

            # Upload files
            if sequential:
                return self.upload_files_sequentially(upload_button_selector, selected_files,
                                                      delay=delay)
            else:
                return self.upload_multiple_files(upload_button_selector, selected_files)

        except Exception as e:
            print(f"Error uploading random files: {e}")
            return False

    def wait_for_upload_completion(self, success_selector=None, timeout=30):
        """
        Wait for upload completion by looking for success indicators

        Args:
            success_selector: CSS selector for success message/indicator
            timeout: Maximum wait time in seconds

        Returns:
            bool: True if success indicator found
        """
        if not success_selector:
            return True

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, success_selector))
            )
            print("Upload completion confirmed!")
            return True
        except:
            print("Upload completion not detected within timeout")
            return False

    def close(self):
        """Close the WebDriver if it was created by this class"""
        if self.should_quit_driver and self.driver:
            self.driver.quit()
            print("WebDriver closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
