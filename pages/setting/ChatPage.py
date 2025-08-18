from datetime import datetime

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import time
from base.base_driver import BaseDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.ValidationControls import ValidationControls
from utilities.utils import Utils
from utilities.web_element import WebItem
from selenium.webdriver.common.keys import Keys
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
    def chat_single_question(self,record_test,number_of_chat):
        user_query_text_control = self.find_element(By.CLASS_NAME,"chat-input")
        div_control = user_query_text_control.find_element(By.ID,"chat-input")
        self.web_elements.enter_web_item_text(div_control,record_test['question'])
        start_time = time.time()
        try :
            self.web_elements.press_enter_on_text_control(div_control)
            parent = self.find_element(By.TAG_NAME, "app-chat-chat-content")


            rec = record_test.copy()
            rec['evident'] = None
            button_quotes = WebDriverWait(self.driver, 300).until(
                lambda driver: parent.find_elements(By.XPATH, "//button[contains(@class, 'btn-quote')]")
                if len(parent.find_elements(By.XPATH, "//button[contains(@class, 'btn-quote')]")) == number_of_chat
                else False
            )
            screen_shot = self.take_screenshot()
            item_contents = parent.find_elements(By.XPATH, "//div[contains(@class,'bubble-item-assistant')]")
            end_time = time.time()
            elapsed_time = end_time - start_time
            if len(item_contents[-1].text.strip()) == 0:
                rec['actual_answer'] = ""
                rec['test_result'] = "fail"
                rec['evident'] = screen_shot
            else:
                rec['actual_answer'] = item_contents[-1].text
                rec['test_result'] = "pass"
            rec['time_response'] = str(elapsed_time) + " second(s)"
            button_quotes[-1].click()
            time.sleep(5)
            div_contents = self.find_element(By.XPATH,"//div[contains(@class, 'modal-body scroll')]")
            rec['context'] = div_contents.text
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        except Exception as e:
            print(e)
            rec['actual_answer'] = ""
            rec['test_result'] = "fail"
            rec['time_response'] = "exceed 5 minutes"
            rec['context'] = ""
            rec['evident'] = screen_shot
        return rec

    def set_model_name(self,model_name):
        button_dropdown = self.find_element(By.XPATH, self.BUTTON_DROP_DOWN)
        button_dropdown.click()
        self.get_dropdown_item_by_name(model_name)
    def chat_with_model(self,model_name,data):
        if model_name != "":
            button_dropdown = self.find_element(By.XPATH, self.BUTTON_DROP_DOWN)
            button_dropdown.click()
            self.get_dropdown_item_by_name(model_name)
        lst_result = []
        number_of_chat = 0
        for record_test in data:
            rect = record_test.copy()
            rect['model'] = model_name
            return_record = self.chat_single_question(rect,number_of_chat+1)
            time.sleep(4)
            lst_result.append(return_record)
            number_of_chat = number_of_chat + 1
        return lst_result

    def enter_new_chat(self):
        chat_create_button = self.find_element(By.XPATH, self.BUTTON_NEW_CHAT)
        chat_create_button.click()
        time.sleep(1)
