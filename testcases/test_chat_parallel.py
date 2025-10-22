"""
Parallel ChatBot Testing Module

This module provides parallel testing capabilities for chatbot performance testing
with multiple concurrent users.
"""

import os
import random
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from pages.login import Login
from pages.ChatBotPage import ChatBotPage
from utilities.ReadData import ReadChatData
from utilities.ChatBotResultWriter import export_chatbot_results

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
BASE_DIR_TEST_RESULT = "./test_results"
DATA_TEST_FILE = "./testdata/test_search_rag_samco.xlsx"
CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"  # Update this path


class ParallelChatBotTester:
    """
    Parallel ChatBot Performance Tester

    This class manages parallel testing of chatbot with multiple users
    to evaluate system performance under load.
    """

    def __init__(
        self,
        base_url: str,
        data_file: str = DATA_TEST_FILE,
        chrome_driver_path: str = CHROME_DRIVER_PATH,
        headless: bool = True
    ):
        """
        Initialize the parallel tester

        Args:
            base_url: Base URL of the application
            data_file: Path to test data Excel file
            chrome_driver_path: Path to ChromeDriver executable
            headless: Run browsers in headless mode
        """
        self.base_url = base_url
        self.data_file = data_file
        self.chrome_driver_path = chrome_driver_path
        self.headless = headless

        # Load test data
        dataobj = ReadChatData(data_file_name=data_file)
        self.test_data = dataobj.read_data()

        # Create results directory
        os.makedirs(BASE_DIR_TEST_RESULT, exist_ok=True)

        logger.info(f"ParallelChatBotTester initialized with {len(self.test_data)} test questions")

    def _create_driver(self) -> webdriver.Chrome:
        """
        Create a new WebDriver instance

        Returns:
            Chrome WebDriver instance
        """
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = Service(self.chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)

        return driver

    def _test_single_user(
        self,
        user_name: str,
        password: str,
        num_questions: int = 3,
        model_name: str = ""
    ) -> Tuple[str, bool, List[Dict]]:
        """
        Test chatbot with a single user

        Args:
            user_name: Username for login
            password: Password for login
            num_questions: Number of questions to test
            model_name: Model to use for testing

        Returns:
            Tuple of (username, success, results)
        """
        driver = None
        results = []
        success = False

        try:
            logger.info(f"Starting test for user: {user_name}")

            # Create driver
            driver = self._create_driver()
            driver.get(self.base_url)

            # Login
            login_page = Login(driver)
            hp, error = login_page.do_login(user_name=user_name, pass_word=password)

            if error:
                logger.error(f"Login failed for {user_name}: {error}")
                return user_name, False, []

            # Navigate to chat
            setting = hp.get_setting_menu()
            chat_window = setting.get_chat_menu()

            # Initialize ChatBotPage
            chatbot_page = ChatBotPage(driver)

            # Select random questions
            random_questions = random.sample(
                self.test_data,
                min(num_questions, len(self.test_data))
            )

            # Run tests
            logger.info(f"Testing {len(random_questions)} questions for {user_name}")
            results = chatbot_page.test_multiple_questions(
                questions_data=random_questions,
                model_name=model_name
            )

            # Save results
            file_name = os.path.join(
                BASE_DIR_TEST_RESULT,
                f"{user_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            export_chatbot_results(results, filename=file_name)

            logger.info(f"Test completed for {user_name}. Results saved to {file_name}")
            success = True

        except Exception as e:
            logger.error(f"Error testing user {user_name}: {e}")
            success = False

        finally:
            if driver:
                driver.quit()

        return user_name, success, results

    def run_parallel_tests(
        self,
        user_credentials: List[Tuple[str, str]],
        num_questions: int = 3,
        model_name: str = "",
        max_workers: int = 10
    ) -> Dict[str, any]:
        """
        Run parallel tests with multiple users

        Args:
            user_credentials: List of (username, password) tuples
            num_questions: Number of questions per user
            model_name: Model to use for testing
            max_workers: Maximum number of parallel workers

        Returns:
            Dictionary with test summary
        """
        logger.info(f"Starting parallel test with {len(user_credentials)} users")
        logger.info(f"Max workers: {max_workers}, Questions per user: {num_questions}")

        start_time = datetime.now()
        all_results = []
        success_count = 0
        failed_count = 0

        # Use ThreadPoolExecutor for parallel execution
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_user = {
                executor.submit(
                    self._test_single_user,
                    user_name,
                    password,
                    num_questions,
                    model_name
                ): user_name
                for user_name, password in user_credentials
            }

            # Process completed tasks
            for future in as_completed(future_to_user):
                user_name = future_to_user[future]
                try:
                    username, success, results = future.result()

                    if success:
                        success_count += 1
                        all_results.extend(results)
                        logger.info(f"✓ {username} completed successfully")
                    else:
                        failed_count += 1
                        logger.warning(f"✗ {username} failed")

                except Exception as e:
                    logger.error(f"Exception for {user_name}: {e}")
                    failed_count += 1

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Generate summary
        summary = {
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_seconds": duration,
            "total_users": len(user_credentials),
            "successful_users": success_count,
            "failed_users": failed_count,
            "total_tests": len(all_results),
            "passed_tests": sum(1 for r in all_results if r.get("test_result") == "pass"),
            "failed_tests": sum(1 for r in all_results if r.get("test_result") == "fail"),
            "questions_per_user": num_questions,
            "max_workers": max_workers
        }

        # Save consolidated summary
        self._save_summary(summary, all_results)

        logger.info("=" * 80)
        logger.info("PARALLEL TEST SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Total Users: {summary['total_users']}")
        logger.info(f"Successful Users: {summary['successful_users']}")
        logger.info(f"Failed Users: {summary['failed_users']}")
        logger.info(f"Total Tests: {summary['total_tests']}")
        logger.info(f"Passed Tests: {summary['passed_tests']}")
        logger.info(f"Failed Tests: {summary['failed_tests']}")
        logger.info("=" * 80)

        return summary

    def _save_summary(self, summary: Dict, all_results: List[Dict]):
        """
        Save consolidated test summary

        Args:
            summary: Summary statistics
            all_results: All test results
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_file = os.path.join(
            BASE_DIR_TEST_RESULT,
            f"parallel_test_summary_{timestamp}.xlsx"
        )

        try:
            # Create summary DataFrame
            summary_df = pd.DataFrame([summary])
            summary_df.to_excel(summary_file, sheet_name="Summary", index=False)

            logger.info(f"Summary saved to {summary_file}")

        except Exception as e:
            logger.error(f"Failed to save summary: {e}")


def generate_user_credentials(base_name: str, start_num: int, count: int, password: str = "123456") -> List[Tuple[str, str]]:
    """
    Generate list of user credentials

    Args:
        base_name: Base username (e.g., "auto_user")
        start_num: Starting number
        count: Number of users to generate
        password: Password for all users

    Returns:
        List of (username, password) tuples
    """
    return [
        (f"{base_name}{str(start_num + i).zfill(4)}", password)
        for i in range(count)
    ]


# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parallel ChatBot Performance Testing")
    parser.add_argument("--url", required=True, help="Base URL of the application")
    parser.add_argument("--users", type=int, default=20, help="Number of users (default: 20)")
    parser.add_argument("--start-num", type=int, default=80, help="Starting user number (default: 80)")
    parser.add_argument("--questions", type=int, default=3, help="Questions per user (default: 3)")
    parser.add_argument("--workers", type=int, default=10, help="Max parallel workers (default: 10)")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")

    args = parser.parse_args()

    # Generate user credentials
    user_credentials = generate_user_credentials(
        base_name="auto_user",
        start_num=args.start_num,
        count=args.users,
        password="123456"
    )

    # Initialize tester
    tester = ParallelChatBotTester(
        base_url=args.url,
        headless=args.headless
    )

    # Run parallel tests
    summary = tester.run_parallel_tests(
        user_credentials=user_credentials,
        num_questions=args.questions,
        max_workers=args.workers
    )

    print("\nTest completed successfully!")
    print(f"Results saved to: {BASE_DIR_TEST_RESULT}")
