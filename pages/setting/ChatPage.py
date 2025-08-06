from datetime import datetime

from selenium.webdriver.common.by import By

import time
from base.base_driver import BaseDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.ValidationControls import ValidationControls
from utilities.utils import Utils
from utilities.web_element import WebItem
# every chat bot must answer in 3 seconds
DEAD_LINE_TIME = 120


class element_has_children(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            children = element.find_elements(By.XPATH, "./*")
            return element if children else False
        except:
            return False
class ChatPage(BaseDriver):
    BUTTON_NEW_CHAT = "/html/body/app-root/app-admin-layout/div/main/app-chat-main/div/div/app-chat-sidebar/div/div/div/div[1]/button[1]"
    BUTTON_DROP_DOWN = "/html/body/app-root/app-admin-layout/div/main/app-chat-main/div/div/div/div/div/div[2]/div[1]/button"
    USER_QUERY_TEXT = "/html/body/app-root/app-admin-layout/div/main/app-chat-main/div/div/div/div/div[2]/app-chat-chat-box/div/div/div[3]"
    DROPDOWN_CONTENT = "/html/body/app-root/app-admin-layout/div/main/app-chat-main/div/div/div/div/div/div[2]/div[1]/ul"

    def __init__(self,driver):
        super().__init__(driver)
        self.ut = Utils()
        self.web_elements = WebItem(driver)
    def get_dropdown_item_by_name(self,drop_down_item_text):
        time.sleep(1)
        dropdown_content = self.find_element(By.XPATH,self.DROPDOWN_CONTENT)
        links = dropdown_content.find_elements(By.TAG_NAME,"a")
        for link in links:
            if link.text == drop_down_item_text:
                link.click()
                break
    def chat_single_question(self,record_test):
        user_query_text_control = self.find_element(By.CLASS_NAME,"chat-input")
        div_control = user_query_text_control.find_element(By.ID,"chat-input")
        self.web_elements.enter_web_item_text(div_control,record_test['question'])
        start_time = time.time()
        try :
            self.web_elements.press_enter_on_text_control(div_control)
            parent = WebDriverWait(self.driver,DEAD_LINE_TIME).until(
                element_has_children((By.XPATH, "//markdown[@class='hljs text-break']"))
            )
            end_time = time.time()
            elapsed_time = end_time - start_time
            record_test['actual_answer'] = parent.text
            record_test['test_result'] = "pass"
            record_test['time_response'] = str(elapsed_time) + " second(s)"
            grant_parent = parent.find_element(By.XPATH, "..")
            button_quotes = grant_parent.find_elements(By.XPATH, "//button[contains(@class, 'btn-quote')]")
            button_quotes[-1].click()
            div_contents = self.find_element(By.XPATH,"//div[@class='rounded-4 border p-4 scroll-y mb-3']")


            paragraphs = div_contents.find_elements(By.TAG_NAME,"p")
            record_test['context'] = paragraphs[-1].text

        except:
            record_test['actual_answer'] = ""
            record_test['test_result'] = "fail"
            record_test['time_response'] = "exceed 5 minutes"
            record_test['context'] = ""
            record_test['screen_shot'] = self.take_screenshot()
        return record_test

    def set_model_name(self,model_name):
        button_dropdown = self.find_element(By.XPATH, self.BUTTON_DROP_DOWN)
        button_dropdown.click()
        self.get_dropdown_item_by_name(model_name)
    def chat_with_model(self,model_name,data):
        button_dropdown = self.find_element(By.XPATH, self.BUTTON_DROP_DOWN)
        button_dropdown.click()
        self.get_dropdown_item_by_name(model_name)
        lst_result = []
        for record_test in data:
            record_test['model'] = model_name
            return_record = self.chat_single_question(record_test=record_test)
            time.sleep(15)
            lst_result.append(return_record)
        return lst_result

    def enter_new_chat(self):
        chat_create_button = self.find_element(By.XPATH, self.BUTTON_NEW_CHAT)
        chat_create_button.click()
        time.sleep(1)
