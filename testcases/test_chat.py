import datetime
import os.path
import random
from datetime import datetime,timedelta
import pandas as pd
import pytest
import softest
import time
from utilities.ChatBotResultWriter import export_chatbot_results
from utilities.ReadData import ReadChatData
from utilities.customLogger import LogGen
from pages.login import Login
from pages.ChatBotPage import ChatBotPage
from utilities.utils import Utils

BASE_DIR_TEST_RESULT = "./test_results"
DATA_TEST_FILE = "./testdata/test_search_rag_samco.xlsx"

@pytest.mark.usefixtures("setup")
@pytest.mark.test_chat
class TestAiKnow(softest.TestCase):
    logger = LogGen.loggen()

    @pytest.fixture(autouse=True)
    def class_setup(self, user_account):
        self.login = Login(self.driver)
        self.ut = Utils()
        self.user_account = user_account
        dataobj = ReadChatData(data_file_name=DATA_TEST_FILE)
        self.dataset = dataobj.read_data()

    def chat_with_user(self, user_name, pass_word, num_questions=3):
        """
        Test chatbot with specific user

        Args:
            user_name: Username for login
            pass_word: Password for login
            num_questions: Number of random questions to test (default: 3)
        """
        # Login
        hp, error = self.login.do_login(user_name=user_name, pass_word=pass_word)
        if error != "":
            self.logger.error(f"Login failed for {user_name}: {error}")
            return

        # Navigate to chat
        setting = hp.get_setting_menu()
        chat_window = setting.get_chat_menu()

        # Initialize ChatBotPage
        chatbot_page = ChatBotPage(self.driver)

        # Select random questions for testing
        random_questions = random.sample(self.dataset, min(num_questions, len(self.dataset)))

        # Configure model (empty string for default model)
        MODEL_NAME = ""  # Or specify model like "Claude 4 Sonnet-Reasoning"

        # Run tests
        self.logger.info(f"Starting chat test for {user_name} with {len(random_questions)} questions")
        test_results = chatbot_page.test_multiple_questions(
            questions_data=random_questions,
            model_name=MODEL_NAME
        )

        # Create output directory if it doesn't exist
        os.makedirs(BASE_DIR_TEST_RESULT, exist_ok=True)

        # Save results to Excel
        file_name = os.path.join(BASE_DIR_TEST_RESULT, f"{user_name}.xlsx")
        export_chatbot_results(test_results, filename=file_name)

        self.logger.info(f"Test results saved to {file_name}")

        return test_results
    def test_with_user_1(self):
        user_name = "auto_user0080"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_2(self):
        user_name = "auto_user0081"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_3(self):
        user_name = "auto_user0082"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_4(self):
        user_name = "auto_user0083"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_5(self):
        user_name = "auto_user0084"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)

    """
    
    def test_with_user_6(self):
        user_name = "auto_user0006"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_7(self):
        user_name = "auto_user0007"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_8(self):
        user_name = "auto_user0008"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_9(self):
        user_name = "auto_user0009"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_10(self):
        user_name = "auto_user0010"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_11(self):
        user_name = "auto_user0011"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_12(self):
        user_name = "auto_user0012"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_13(self):
        user_name = "auto_user0013"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_14(self):
        user_name = "auto_user0014"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_15(self):
        user_name = "auto_user0015"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_16(self):
        user_name = "auto_user0016"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_17(self):
        user_name = "auto_user0017"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_18(self):
        user_name = "auto_user0018"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_19(self):
        user_name = "auto_user0019"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_20(self):
        user_name = "auto_user0020"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_21(self):
        user_name = "auto_user0021"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_22(self):
        user_name = "auto_user0022"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_23(self):
        user_name = "auto_user0023"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_24(self):
        user_name = "auto_user0024"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_25(self):
        user_name = "auto_user0025"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_26(self):
        user_name = "auto_user0026"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_27(self):
        user_name = "auto_user0027"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_28(self):
        user_name = "auto_user0028"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_29(self):
        user_name = "auto_user0029"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_30(self):
        user_name = "auto_user0030"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_31(self):
        user_name = "auto_user0031"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_32(self):
        user_name = "auto_user0032"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_33(self):
        user_name = "auto_user0033"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_34(self):
        user_name = "auto_user0034"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_35(self):
        user_name = "auto_user0035"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_36(self):
        user_name = "auto_user0036"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_37(self):
        user_name = "auto_user0037"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_38(self):
        user_name = "auto_user0038"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_39(self):
        user_name = "auto_user0039"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_40(self):
        user_name = "auto_user0040"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_41(self):
        user_name = "auto_user0041"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_42(self):
        user_name = "auto_user0042"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_43(self):
        user_name = "auto_user0043"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_44(self):
        user_name = "auto_user0044"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_45(self):
        user_name = "auto_user0045"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_46(self):
        user_name = "auto_user0046"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_47(self):
        user_name = "auto_user0047"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_48(self):
        user_name = "auto_user0048"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_49(self):
        user_name = "auto_user0049"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_50(self):
        user_name = "auto_user0050"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_51(self):
        user_name = "auto_user0051"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_52(self):
        user_name = "auto_user0052"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_53(self):
        user_name = "auto_user0053"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_54(self):
        user_name = "auto_user0054"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_55(self):
        user_name = "auto_user0055"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_56(self):
        user_name = "auto_user0056"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_57(self):
        user_name = "auto_user0057"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_58(self):
        user_name = "auto_user0058"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_59(self):
        user_name = "auto_user0059"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_60(self):
        user_name = "auto_user0060"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_61(self):
        user_name = "auto_user0061"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_62(self):
        user_name = "auto_user0062"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_63(self):
        user_name = "auto_user0063"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_64(self):
        user_name = "auto_user0064"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_65(self):
        user_name = "auto_user0065"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_66(self):
        user_name = "auto_user0066"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_67(self):
        user_name = "auto_user0067"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_68(self):
        user_name = "auto_user0068"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_69(self):
        user_name = "auto_user0069"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_70(self):
        user_name = "auto_user0070"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_71(self):
        user_name = "auto_user0071"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_72(self):
        user_name = "auto_user0072"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_73(self):
        user_name = "auto_user0073"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_74(self):
        user_name = "auto_user0074"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_75(self):
        user_name = "auto_user0075"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_76(self):
        user_name = "auto_user0076"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_77(self):
        user_name = "auto_user0077"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_78(self):
        user_name = "auto_user0078"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_79(self):
        user_name = "auto_user0079"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_80(self):
        user_name = "auto_user0080"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_81(self):
        user_name = "auto_user0081"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_82(self):
        user_name = "auto_user0082"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_83(self):
        user_name = "auto_user0083"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_84(self):
        user_name = "auto_user0084"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_85(self):
        user_name = "auto_user0085"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_86(self):
        user_name = "auto_user0086"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_87(self):
        user_name = "auto_user0087"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_88(self):
        user_name = "auto_user0088"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_89(self):
        user_name = "auto_user0089"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_90(self):
        user_name = "auto_user0090"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_91(self):
        user_name = "auto_user0091"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name,pass_word=pass_word)
    def test_with_user_92(self):
        user_name = "auto_user0092"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_93(self):
        user_name = "auto_user0093"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_94(self):
        user_name = "auto_user0094"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_95(self):
        user_name = "auto_user0095"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_96(self):
        user_name = "auto_user0096"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_97(self):
        user_name = "auto_user0097"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_98(self):
        user_name = "auto_user0098"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_99(self):
        user_name = "auto_user0099"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
    def test_with_user_100(self):
        user_name = "auto_user0100"
        pass_word = "123456"
        self.chat_with_user(user_name=user_name, pass_word=pass_word)
"""