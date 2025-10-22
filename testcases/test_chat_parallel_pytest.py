"""
Pytest-compatible Parallel ChatBot Testing

This module provides pytest integration for parallel chatbot testing
"""

import os
import random
import pytest
from pages.login import Login
from pages.ChatBotPage import ChatBotPage
from utilities.ReadData import ReadChatData
from utilities.ChatBotResultWriter import export_chatbot_results
from utilities.customLogger import LogGen

BASE_DIR_TEST_RESULT = "./test_results"
DATA_TEST_FILE = "./testdata/test_search_rag_samco.xlsx"

# User list for parallel testing (20 users)
PARALLEL_TEST_USERS = [
    ("auto_user0080", "123456"),
    ("auto_user0081", "123456"),
    ("auto_user0082", "123456"),
    ("auto_user0083", "123456"),
    ("auto_user0084", "123456"),
    ("auto_user0085", "123456"),
    ("auto_user0086", "123456"),
    ("auto_user0087", "123456"),
    ("auto_user0088", "123456"),
    ("auto_user0089", "123456"),
    ("auto_user0090", "123456"),
    ("auto_user0091", "123456"),
    ("auto_user0092", "123456"),
    ("auto_user0093", "123456"),
    ("auto_user0094", "123456"),
    ("auto_user0095", "123456"),
    ("auto_user0096", "123456"),
    ("auto_user0097", "123456"),
    ("auto_user0098", "123456"),
    ("auto_user0099", "123456"),
]


@pytest.mark.usefixtures("setup")
@pytest.mark.test_chat_parallel
@pytest.mark.parametrize("user_name,password", PARALLEL_TEST_USERS)
class TestChatBotParallel:
    """
    Parallel ChatBot Test Class

    Run with: pytest -v -n 10 -m test_chat_parallel testcases/test_chat_parallel_pytest.py

    Options:
        -n 10: Run with 10 parallel workers (adjust based on system resources)
        -m test_chat_parallel: Run only parallel chat tests
        -v: Verbose output
    """

    logger = LogGen.loggen()

    @pytest.fixture(autouse=True)
    def class_setup(self, user_account):
        """Setup test data"""
        self.login = Login(self.driver)
        dataobj = ReadChatData(data_file_name=DATA_TEST_FILE)
        self.dataset = dataobj.read_data()

        # Create results directory
        os.makedirs(BASE_DIR_TEST_RESULT, exist_ok=True)

    def test_chatbot_performance(self, user_name, password):
        """
        Test chatbot performance with specific user

        This test will be executed in parallel for all users in PARALLEL_TEST_USERS

        Args:
            user_name: Username from parametrize
            password: Password from parametrize
        """
        self.logger.info(f"Starting parallel test for {user_name}")

        try:
            # Login
            hp, error = self.login.do_login(user_name=user_name, pass_word=password)

            if error:
                self.logger.error(f"Login failed for {user_name}: {error}")
                pytest.fail(f"Login failed: {error}")

            # Navigate to chat
            setting = hp.get_setting_menu()
            chat_window = setting.get_chat_menu()

            # Initialize ChatBotPage
            chatbot_page = ChatBotPage(self.driver)

            # Select random questions (3 per user for performance testing)
            num_questions = 3
            random_questions = random.sample(
                self.dataset,
                min(num_questions, len(self.dataset))
            )

            # Run tests
            MODEL_NAME = ""  # Use default model
            test_results = chatbot_page.test_multiple_questions(
                questions_data=random_questions,
                model_name=MODEL_NAME
            )

            # Save results
            file_name = os.path.join(BASE_DIR_TEST_RESULT, f"parallel_{user_name}.xlsx")
            export_chatbot_results(test_results, filename=file_name)

            self.logger.info(f"Test completed for {user_name}. Results: {file_name}")

            # Assert that at least some tests passed
            passed_tests = sum(1 for r in test_results if r.get("test_result") == "pass")
            assert passed_tests > 0, f"No tests passed for {user_name}"

        except Exception as e:
            self.logger.error(f"Error testing {user_name}: {e}")
            pytest.fail(f"Test failed: {str(e)}")


# Single user tests (can be run individually or together)
@pytest.mark.usefixtures("setup")
@pytest.mark.test_chat_single
class TestChatBotSingle:
    """
    Single User ChatBot Tests

    Run with: pytest -v -m test_chat_single testcases/test_chat_parallel_pytest.py
    """

    logger = LogGen.loggen()

    @pytest.fixture(autouse=True)
    def class_setup(self, user_account):
        """Setup test data"""
        self.login = Login(self.driver)
        dataobj = ReadChatData(data_file_name=DATA_TEST_FILE)
        self.dataset = dataobj.read_data()
        os.makedirs(BASE_DIR_TEST_RESULT, exist_ok=True)

    def _test_user(self, user_name, password, num_questions=3):
        """
        Helper method to test a single user

        Args:
            user_name: Username
            password: Password
            num_questions: Number of questions to test
        """
        self.logger.info(f"Testing user: {user_name}")

        # Login
        hp, error = self.login.do_login(user_name=user_name, pass_word=password)

        if error:
            self.logger.error(f"Login failed for {user_name}: {error}")
            return

        # Navigate to chat
        setting = hp.get_setting_menu()
        chat_window = setting.get_chat_menu()

        # Initialize ChatBotPage
        chatbot_page = ChatBotPage(self.driver)

        # Select random questions
        random_questions = random.sample(
            self.dataset,
            min(num_questions, len(self.dataset))
        )

        # Run tests
        MODEL_NAME = ""
        test_results = chatbot_page.test_multiple_questions(
            questions_data=random_questions,
            model_name=MODEL_NAME
        )

        # Save results
        file_name = os.path.join(BASE_DIR_TEST_RESULT, f"{user_name}.xlsx")
        export_chatbot_results(test_results, filename=file_name)

        self.logger.info(f"Test completed for {user_name}")

    def test_user_0080(self):
        """Test with auto_user0080"""
        self._test_user("auto_user0080", "123456")

    def test_user_0081(self):
        """Test with auto_user0081"""
        self._test_user("auto_user0081", "123456")

    def test_user_0082(self):
        """Test with auto_user0082"""
        self._test_user("auto_user0082", "123456")

    def test_user_0083(self):
        """Test with auto_user0083"""
        self._test_user("auto_user0083", "123456")

    def test_user_0084(self):
        """Test with auto_user0084"""
        self._test_user("auto_user0084", "123456")
