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
ERROR_CLASS_NAME = "form-text text-danger"
class UserManagement(BaseDriver):
    APP_USER_LIST_TAG = "app-user-list"
    APP_USER_ADD_MODAL = "app-user-add-modal"
    def __init__(self,driver):
        super().__init__(driver)
        self.ut = Utils()
        self.web_elements = WebItem(driver)
        self.validate_control = ValidationControls(driver=driver)
        app_user_main = self.find_element(By.TAG_NAME,self.APP_USER_LIST_TAG)
        self.child_divs = app_user_main.find_elements(By.TAG_NAME, "div")
    def open_add_user(self):
        button_add = self.child_divs[0].find_element(By.TAG_NAME,"button")
        button_add.click()
        time.sleep(2)
        modal_add_dialog = self.find_element(By.CLASS_NAME,"modal-content")
        form_add_new = modal_add_dialog.find_element(By.TAG_NAME,"form")
        self.div_addnew_controls = form_add_new.find_elements(By.TAG_NAME,"div")
    def validate_username(self,text_to_validate):
        element = self.find_element(By.CSS_SELECTOR,
                                      "input[type='text'][formcontrolname='username']")
        self.validate_control.validate_single_control(element,text_input=text_to_validate)
        txt_error = ""
        parent = element.find_element(By.XPATH, "..")
        # find an error text
        try :
            error_div = parent.find_element(By.CLASS_NAME,ERROR_CLASS_NAME)
            txt_error = error_div.text
            ret = "nok"
        except:
            ret = "ok"
        return  ret, txt_error

    def valiadte_email(self,text_to_validate):
        self.validate_control.validation_input_control(self.div_addnew_controls[0], text_to_validate)



