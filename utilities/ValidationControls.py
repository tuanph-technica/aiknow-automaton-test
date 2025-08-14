from base.base_driver import BaseDriver
from utilities.web_element import WebItem
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class ValidationControls(BaseDriver):
    def __init__(self,driver):
        super().__init__(driver)
        self.web_item = WebItem(driver)
    def validation_input_control(self,element_group,text_input,error_tag="mat-error"):
        input_web = element_group.find_element(By.TAG_NAME,"input")
        self.web_item.enter_web_item_text(input_web,text_input)
        input_web.send_keys(Keys.TAB)
        try :
            validation_error = element_group.find_element(By.TAG_NAME, error_tag)
            return False, validation_error.text
        except:
            return True, ""
    def validate_single_control(self,web_item,text_input,error_tag='mat-error'):
        self.web_item.enter_web_item_text(web_item, text_input)
        web_item.send_keys(Keys.TAB)









