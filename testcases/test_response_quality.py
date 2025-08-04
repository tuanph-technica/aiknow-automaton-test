import datetime
import random
from datetime import datetime,timedelta
import pandas as pd
import pytest
import softest
import time
from utilities.ExcelImageWriter import export_data_to_excel
from utilities.ReadData import ReadChatData, ChatResponseData
from utilities.chatbotscoring import OllamaChatbotScorer
from utilities.customLogger import LogGen
from pages.login import Login
from utilities.japanese_extractor import extract_nouns_verbs_ginza
from utilities.utils import Utils
#DATA_TEST_FILE = "../testdata/test_search_rag_samco.xlsx"
DATA_TEST_FILE = "../testdata/case_auto test KQ RAG.xlsx"
@pytest.mark.test_response_quality
class TestChatQuality(softest.TestCase):
    logger = LogGen.loggen()
    def test_and_score_response(self):
        chat_response_data_obj = ChatResponseData(DATA_TEST_FILE)
        records = chat_response_data_obj.read_data()
        scorer = OllamaChatbotScorer(model_name="llama3.2:latest")
        scoring_result = []
        for record in records:
            user_question = record['question']
            actual_response = record['actual_result_1']
            expected_response = record['expected_result']
            keyword = record['keyword']
            keywords = extract_nouns_verbs_ginza(keyword)
            evaluation = scorer.score_response(
                user_question=user_question,
                actual_response=actual_response,
                expected_response=expected_response,
                keywords=keywords,
                keyword_matching_threshold=70.0  # Must have at least 70% of keywords
            )
            scoring_result.append(evaluation)
            actual_response = record['actual_result_2']
            evaluation = scorer.score_response(
                user_question=user_question,
                actual_response=actual_response,
                expected_response=expected_response,
                keywords=keywords,
                keyword_matching_threshold=70.0  # Must have at least 70% of keywords
            )
            scoring_result.append(evaluation)
            actual_response = record['actual_result_3']
            evaluation = scorer.score_response(
                user_question=user_question,
                actual_response=actual_response,
                expected_response=expected_response,
                keywords=keywords,
                keyword_matching_threshold=20.0  # Must have at least 70% of keywords
            )
            scoring_result.append(evaluation)
            actual_response = record['actual_result_4']
            evaluation = scorer.score_response(
                user_question=user_question,
                actual_response=actual_response,
                expected_response=expected_response,
                keywords=keywords,
                keyword_matching_threshold=70.0  # Must have at least 70% of keywords
            )
            scoring_result.append(evaluation)
            actual_response = record['actual_result_5']
            evaluation = scorer.score_response(
                user_question=user_question,
                actual_response=actual_response,
                expected_response=expected_response,
                keywords=keywords,
                keyword_matching_threshold=70.0  # Must have at least 70% of keywords
            )
            scoring_result.append(evaluation)
        return scoring_result








