import datetime
import random
from datetime import datetime,timedelta
import pandas as pd
import pytest
import softest
import time
from utilities.ExcelImageWriter import export_data_to_excel
from utilities.ReadData import ReadChatData, UserManagementData
from utilities.customLogger import LogGen
from pages.login import Login
from utilities.utils import Utils
DATA_TEST_FILE = "../testdata/user_management.xlsx"
@pytest.mark.usefixtures("setup")
@pytest.mark.test_user_management
class TestUserManagement(softest.TestCase):
    logger = LogGen.loggen()
    @pytest.fixture(autouse=True)
    def class_setup(self, user_account):
        self.login = Login(self.driver)
        self.ut = Utils()
        self.user_account = user_account
    def validate_add_user(self):
        user_name = "auto_user0008"
        pass_word = "123456"
        hp, error = self.login.do_login(user_name=user_name,
                                        pass_word=pass_word)
        user_management_page = hp.get_user_management_menu()
        user_management_page.open_add_user(user_obj=None)
        dataset_obj = UserManagementData(DATA_TEST_FILE)
        validation_dataset = dataset_obj.read_data(sheet_name="validation")
        for validation_object in validation_dataset:
            validation_control_name = validation_object['validation_control_name']
            if validation_control_name == "user_name":
                txt_validation = validation_object['user_name']
                user_management_page.validate_username(txt_validation)
            elif validation_control_name == "email":
                txt_validation = validation_object['email']
                user_management_page.valiadte_email(txt_validation)






