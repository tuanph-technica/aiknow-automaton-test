import datetime
import glob
import os
import random
from datetime import datetime,timedelta
import pandas as pd
import pytest
import softest
import time
from utilities.ExcelImageWriter import export_data_to_excel
from utilities.ReadData import ReadChatData
from utilities.customLogger import LogGen
from pages.login import Login
from utilities.utils import Utils
BASE_PATH = "../testdata/document_upload_files"
CATEGORIES = ["Report","Jounal","Manualfacturing Report"]
def get_upload_files():
    search_pattern = os.path.join(BASE_PATH,"*")
    all_items = glob.glob(search_pattern)
    files = [item for item in all_items if os.path.isfile(item)]
    return files

@pytest.mark.usefixtures("setup")
@pytest.mark.test_documents
class TestDocuments(softest.TestCase):

    logger = LogGen.loggen()
    @pytest.fixture(autouse=True)

    def class_setup(self, user_account):
        self.login = Login(self.driver)
        self.ut = Utils()
        self.user_account = user_account
        self.upload_files = get_upload_files()
    def test_upload_documents(self,num_file=1):
        user_name = "auto_user0001"
        pass_word = "123456"
        hp, error = self.login.do_login(user_name=user_name,
                                        pass_word=pass_word)
        setting = hp.get_setting_menu()
        document_window = setting.get_documents_menu()
        files_upload = get_upload_files()
        random_index = random.randint(0,len(files_upload)-1)
        random_category = random.randint(0,2)
        category_name = CATEGORIES[random_category]

        ret = document_window.open_select_file_dialog(files_upload[random_index])
        if ret:
            document_window.process_upload_file(category_name)




