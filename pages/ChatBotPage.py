import time
from datetime import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_driver import BaseDriver
from utilities.utils import Utils
from utilities.web_element import WebItem
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Timeout for chatbot response
RESPONSE_TIMEOUT = 300  # 5 minutes

class ChatBotPage(BaseDriver):
    """
    ChatBot Page Object for automation testing

    This class provides methods to interact with the chatbot interface,
    send questions, retrieve responses, and evaluate answer quality.
    """

    # Locators
    BUTTON_NEW_CHAT = "//button[contains(@class, 'btn') and contains(., '新規チャット')]"
    BUTTON_DROP_DOWN = "//button[contains(@class, 'dropdown-toggle')]"
    CHAT_INPUT_FIELD = "chat-input"
    BUTTON_SEND = "//button[contains(@class, 'chat-input-send')]"
    CHAT_CONTENT_CONTAINER = "//app-chat-chat-content"
    BUBBLE_ITEM_ASSISTANT = "//div[contains(@class,'bubble-item-assistant')]"
    BUBBLE_ITEM_CONTENT = ".//div[contains(@class, 'bubble-item-content')]"
    BUTTON_QUOTE = "//button[contains(@class, 'btn-quote')]"
    MODAL_METADATA = "//div[contains(@class, 'modal-body scroll')]"
    DROPDOWN_CONTENT = "//ul[contains(@class, 'dropdown-menu')]"
    LOADING_SPINNER = "//div[contains(@class, 'spinner-border')]"

    def __init__(self, driver):
        """
        Initialize ChatBotPage with WebDriver

        Args:
            driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.ut = Utils()
        self.web_elements = WebItem(driver)
        logger.info("ChatBotPage initialized")

    def wait_for_loading_complete(self, timeout=10):
        """
        Wait for loading spinner to disappear

        Args:
            timeout: Maximum wait time in seconds
        """
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((By.XPATH, self.LOADING_SPINNER))
            )
        except:
            pass  # No spinner found or already disappeared

    def click_new_chat(self):
        """Click the New Chat button to start a new conversation"""
        try:
            new_chat_btn = self.wait_until_element_is_clickable(By.XPATH, self.BUTTON_NEW_CHAT)
            new_chat_btn.click()
            time.sleep(1)
            logger.info("New chat session started")
        except Exception as e:
            logger.error(f"Failed to click new chat button: {e}")
            raise

    def select_model(self, model_name: str):
        """
        Select a specific AI model from dropdown

        Args:
            model_name: Name of the model to select
        """
        if not model_name or model_name.strip() == "":
            logger.info("No model specified, using default")
            return

        try:
            # Click dropdown button
            dropdown_btn = self.wait_until_element_is_clickable(By.XPATH, self.BUTTON_DROP_DOWN)
            dropdown_btn.click()
            time.sleep(1)

            # Find and click the model option
            dropdown_menu = self.find_element(By.XPATH, self.DROPDOWN_CONTENT)
            links = dropdown_menu.find_elements(By.TAG_NAME, "a")

            for link in links:
                if model_name in link.text:
                    link.click()
                    logger.info(f"Selected model: {model_name}")
                    time.sleep(1)
                    return

            logger.warning(f"Model '{model_name}' not found in dropdown")
        except Exception as e:
            logger.error(f"Failed to select model: {e}")
            raise

    def send_question(self, question: str):
        """
        Send a question to the chatbot

        Args:
            question: The question text to send
        """
        try:
            # Find input field
            input_field = self.find_element(By.ID, self.CHAT_INPUT_FIELD)

            # Clear and enter question
            input_field.clear()
            self.web_elements.enter_web_item_text(input_field, question)

            # Press Enter to send
            self.web_elements.press_enter_on_text_control(input_field)
            logger.info(f"Question sent: {question[:50]}...")

        except Exception as e:
            logger.error(f"Failed to send question: {e}")
            raise

    def wait_for_response(self, expected_response_count: int, timeout=RESPONSE_TIMEOUT):
        """
        Wait for chatbot response to complete

        Args:
            expected_response_count: Expected number of responses in the conversation
            timeout: Maximum wait time in seconds

        Returns:
            bool: True if response received, False if timeout
        """
        try:
            parent = self.find_element(By.TAG_NAME, "app-chat-chat-content")

            # Wait for quote buttons to appear (indicating response complete)
            WebDriverWait(self.driver, timeout).until(
                lambda driver: len(parent.find_elements(By.XPATH, self.BUTTON_QUOTE)) == expected_response_count
            )

            logger.info(f"Response {expected_response_count} received")
            return True

        except Exception as e:
            logger.error(f"Timeout waiting for response: {e}")
            return False

    def get_latest_response(self) -> Dict[str, str]:
        """
        Get the latest chatbot response with context

        Returns:
            Dictionary containing response text and context
        """
        try:
            parent = self.find_element(By.TAG_NAME, "app-chat-chat-content")

            # Get all assistant responses
            assistant_bubbles = parent.find_elements(By.XPATH, self.BUBBLE_ITEM_ASSISTANT)

            if not assistant_bubbles:
                logger.warning("No assistant responses found")
                return {"response": "", "context": "", "all_text": ""}

            # Get the latest response
            latest_bubble = assistant_bubbles[-1]

            # Extract all text from the bubble (for evidence)
            all_text = latest_bubble.text

            # Get response content
            try:
                content_div = latest_bubble.find_element(By.XPATH, self.BUBBLE_ITEM_CONTENT)
                response_text = content_div.text
            except:
                response_text = ""

            # Get context from quote button
            context_text = ""
            try:
                quote_buttons = parent.find_elements(By.XPATH, self.BUTTON_QUOTE)
                if quote_buttons:
                    quote_buttons[-1].click()
                    time.sleep(2)

                    # Get modal content
                    modal_body = self.find_element(By.XPATH, self.MODAL_METADATA)
                    context_text = modal_body.text

                    # Close modal
                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    time.sleep(1)
            except Exception as e:
                logger.warning(f"Failed to get context: {e}")

            return {
                "response": response_text,
                "context": context_text,
                "all_text": all_text
            }

        except Exception as e:
            logger.error(f"Failed to get response: {e}")
            return {"response": "", "context": "", "all_text": ""}

    def evaluate_response_quality(
        self,
        actual_response: str,
        expected_context: str,
        expected_result: str
    ) -> Dict[str, any]:
        """
        Evaluate response quality based on expected values

        Args:
            actual_response: The actual chatbot response
            expected_context: Expected context that should be referenced
            expected_result: Expected answer content

        Returns:
            Dictionary with evaluation results
        """
        evaluation = {
            "passed": False,
            "score": 0.0,
            "context_match": False,
            "answer_match": False,
            "details": ""
        }

        # Check if response is empty
        if not actual_response or len(actual_response.strip()) == 0:
            evaluation["details"] = "Empty response"
            return evaluation

        # Check context match (basic substring check)
        context_match_score = 0
        if expected_context:
            # Check if key terms from expected context appear in response
            context_keywords = set(expected_context.split())
            response_words = set(actual_response.split())

            if context_keywords:
                matching_words = context_keywords.intersection(response_words)
                context_match_score = len(matching_words) / len(context_keywords)
                evaluation["context_match"] = context_match_score > 0.3

        # Check answer match (basic substring check)
        answer_match_score = 0
        if expected_result:
            # Check if key terms from expected result appear in response
            answer_keywords = set(expected_result.split())
            response_words = set(actual_response.split())

            if answer_keywords:
                matching_words = answer_keywords.intersection(response_words)
                answer_match_score = len(matching_words) / len(answer_keywords)
                evaluation["answer_match"] = answer_match_score > 0.3

        # Calculate overall score
        evaluation["score"] = (context_match_score + answer_match_score) / 2

        # Determine if passed (threshold: 0.4)
        evaluation["passed"] = evaluation["score"] >= 0.4

        # Generate details
        evaluation["details"] = f"Context match: {context_match_score:.2f}, Answer match: {answer_match_score:.2f}"

        return evaluation

    def test_single_question(
        self,
        question: str,
        expected_context: str,
        expected_result: str,
        response_number: int,
        model_name: str = ""
    ) -> Dict[str, any]:
        """
        Test a single question and evaluate the response

        Args:
            question: The question to ask
            expected_context: Expected context to be referenced
            expected_result: Expected answer
            response_number: Current response number in conversation
            model_name: Model name for tracking

        Returns:
            Dictionary with test results
        """
        start_time = time.time()

        result = {
            "question": question,
            "expected_context": expected_context,
            "expected_result": expected_result,
            "actual_response": "",
            "actual_context": "",
            "test_result": "fail",
            "time_response": "",
            "model": model_name,
            "evident": None,
            "evaluation_score": 0.0,
            "evaluation_details": ""
        }

        try:
            # Send question
            self.send_question(question)

            # Wait for response
            response_received = self.wait_for_response(response_number)

            # Calculate response time
            end_time = time.time()
            elapsed_time = end_time - start_time
            result["time_response"] = f"{elapsed_time:.2f} seconds"

            if not response_received:
                result["test_result"] = "timeout"
                result["evident"] = self.take_screenshot()
                logger.warning(f"Response timeout for question: {question[:50]}")
                return result

            # Get response
            response_data = self.get_latest_response()
            result["actual_response"] = response_data["response"]
            result["actual_context"] = response_data["context"]

            # Take screenshot for evidence
            result["evident"] = self.take_screenshot()

            # Evaluate quality
            if result["actual_response"]:
                evaluation = self.evaluate_response_quality(
                    result["actual_response"],
                    expected_context,
                    expected_result
                )

                result["evaluation_score"] = evaluation["score"]
                result["evaluation_details"] = evaluation["details"]
                result["test_result"] = "pass" if evaluation["passed"] else "fail"
            else:
                result["test_result"] = "fail"
                result["evaluation_details"] = "Empty response"

            logger.info(f"Test completed: {result['test_result']} (score: {result['evaluation_score']:.2f})")

        except Exception as e:
            logger.error(f"Test execution error: {e}")
            result["test_result"] = "error"
            result["evaluation_details"] = str(e)
            result["evident"] = self.take_screenshot()

        return result

    def test_multiple_questions(
        self,
        questions_data: List[Dict],
        model_name: str = ""
    ) -> List[Dict]:
        """
        Test multiple questions in sequence

        Args:
            questions_data: List of dictionaries with question data
            model_name: Model to use for testing

        Returns:
            List of test results
        """
        results = []

        # Start new chat
        self.click_new_chat()

        # Select model if specified
        if model_name:
            self.select_model(model_name)

        # Test each question
        for idx, question_data in enumerate(questions_data, 1):
            logger.info(f"Testing question {idx}/{len(questions_data)}")

            result = self.test_single_question(
                question=question_data.get("Question (from file OCR txt)", ""),
                expected_context=question_data.get("Expected result (Context from file PDF)", ""),
                expected_result=question_data.get("Expected result (Answer)", ""),
                response_number=idx,
                model_name=model_name
            )

            # Add original test data info
            result["STT"] = question_data.get("STT", idx)
            result["Test Data Describe"] = question_data.get("Test Data Describe", "")
            result["Data Type"] = question_data.get("Data Type", "")

            results.append(result)

            # Wait between questions
            time.sleep(2)

        logger.info(f"Completed testing {len(results)} questions")
        return results
