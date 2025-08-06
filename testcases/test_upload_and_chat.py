import datetime
import random
from datetime import datetime,timedelta
import pandas as pd
import pytest
import softest
import time

from my_sql.base_mysql import DataDocuments
from utilities.ExcelImageWriter import export_data_to_excel
from utilities.ReadData import ReadChatData, ChatResponseData
from utilities.chatbotscoring import OllamaChatbotScorer
from utilities.customLogger import LogGen
from pages.login import Login
import glob
from utilities.japanese_extractor import extract_nouns_verbs_ginza
from utilities.utils import Utils
import os
BASE_PATH = "../testdata/document_upload_files"
CATEGORIES = ["Report","Jounal","Manualfacturing Report"]
def get_upload_files():
    search_pattern = os.path.join(BASE_PATH,"*")
    all_items = glob.glob(search_pattern)
    files = [item for item in all_items if os.path.isfile(item)]
    return files



DATA_TEST_FILE = "../testdata/test_search_rag_samco.xlsx"
@pytest.mark.usefixtures("setup")
@pytest.mark.test_upload_and_chat
class TestUploadAndChat(softest.TestCase):
    logger = LogGen.loggen()
    logger = LogGen.loggen()
    @pytest.fixture(autouse=True)
    def class_setup(self, user_account):
        self.login = Login(self.driver)
        self.ut = Utils()
        self.user_account = user_account
        self.upload_files = get_upload_files()
        data_test_obj = ChatResponseData(DATA_TEST_FILE)
        self.test_dataset = data_test_obj.read_data()
        self.data_base = DataDocuments()
    def test_upload_and_chat(self,num_question = 10):
        user_name = "auto_user0008"
        pass_word = "123456"
        hp, error = self.login.do_login(user_name=user_name,
                                        pass_word=pass_word)
        test_samples = random.sample(self.test_dataset,num_question)
        setting = hp.get_setting_menu()

        document_window = setting.get_documents_menu()

        for test_sample in test_samples:
            file_name = test_sample['file_name'].strip()
            if self.data_base.check_document_exist(document_file_name=file_name) == False:
                filtered = list(filter(lambda x: file_name in x, self.upload_files))
                if filtered:
                    file_upload = filtered[0]
                    random_category = random.randint(0, 2)
                    category_name = CATEGORIES[random_category]
                    ret = document_window.open_select_file_dialog(file_upload)
                    if ret:
                        document_window.process_upload_file(category_name)
                    time.sleep(60)


        chat_window = setting.get_chat_menu()
        chat_window.enter_new_chat()
        MODEL_NAME = "DeepSeek-R1-Distill-Llama-70B-FP8-Agent"
        chat_window.set_model_name(MODEL_NAME)
        extracted_files = self.data_base.get_document_extracted()
        chat_results = []
        for test_sample in test_samples:
            file_name = test_sample['file_name'].strip()
            if file_name in extracted_files:
                chat_result = chat_window.chat_single_question(test_sample)
                chat_results.append(chat_result)
    def test_with_extracted_files(self):
        dataset = self.test_dataset
        extracted_files = self.data_base.get_document_extracted()
        i = 3







