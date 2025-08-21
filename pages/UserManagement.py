import random
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
ROLE_SET = ["System Admin","CEO","User"]
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
    def get_text_box(self,input_type,formcontrol_name):
        element = self.find_element(By.CSS_SELECTOR,
                                    "input[type='" + input_type + "'][formcontrolname='" + formcontrol_name + "']")
        return element

    def validate_text_box(self,input_type,formcontrolname,text_to_validate):
        element = self.find_element(By.CSS_SELECTOR,
                                    "input[type='" + input_type +"'][formcontrolname='" + formcontrolname +  "']")

        self.validate_control.validate_single_control(element, text_input=text_to_validate)
        txt_error = ""
        parent = element.find_element(By.XPATH, "..")
        # find an error text
        try:
            error_div = parent.find_element(By.CLASS_NAME, ERROR_CLASS_NAME)
            txt_error = error_div.text
            ret = "nok"
        except:
            ret = "ok"
        return ret, txt_error
    def validate_username(self,text_to_validate):
        return self.validate_text_box(input_type="text",formcontrolname="username",text_to_validate=text_to_validate)
    def valiadte_email(self,text_to_validate):
        return self.validate_text_box(input_type="email",formcontrolname="email",text_to_validate=text_to_validate)
    def valiadte_first_name_en(self,text_to_validate):
        return self.validate_text_box(input_type="text",formcontrolname="firstNameEn",text_to_validate=text_to_validate)
    def valiadte_last_name_en(self,text_to_validate):
        return self.validate_text_box(input_type="text",formcontrolname="lastNameEn",text_to_validate=text_to_validate)
    def valiadte_first_name(self,text_to_validate):
        return self.validate_text_box(input_type="text",formcontrolname="firstName",text_to_validate=text_to_validate)
    def valiadte_last_name(self,text_to_validate):
        return self.validate_text_box(input_type="text",formcontrolname="lastName",text_to_validate=text_to_validate)
    def select_random_roles(self):
        dropdown_control = self.find_element(By.CLASS_NAME,"choices")
        num_roles = random.randint(1,3)
        roles = random.sample(ROLE_SET,num_roles)
        self.web_elements.choices_items_in_dropdown(dropdown_control=dropdown_control,choice_items=roles)
    def add_user(self,user_obj):
        ret = user_obj.copy()
        txt_username = self.get_text_box(input_type="text",formcontrol_name="username")
        self.web_elements.enter_text(txt_username,user_obj['user_name'])
        txt_email = self.get_text_box(input_type="email", formcontrol_name="email")
        self.web_elements.enter_text(txt_email, user_obj['email'])
        txt_en_first_name = self.get_text_box(input_type="text", formcontrol_name="firstNameEn")
        self.web_elements.enter_text(txt_en_first_name, user_obj['first_name_en'])
        txt_en_last_name = self.get_text_box(input_type="text", formcontrol_name="lastNameEn")
        self.web_elements.enter_text(txt_en_last_name, user_obj['last_name_en'])
        txt_first_name = self.get_text_box(input_type="text", formcontrol_name="firstName")
        self.web_elements.enter_text(txt_first_name, user_obj['first_name_jp'])
        txt_last_name = self.get_text_box(input_type="text", formcontrol_name="lastName")
        self.web_elements.enter_text(txt_last_name, user_obj['last_name_jp'])
        txt_birth_date = self.get_text_box(input_type="text",formcontrol_name="dateOfBirth")
        self.web_elements.enter_text(txt_birth_date,user_obj['date_of_birth'])
        select_element = self.find_element(By.CSS_SELECTOR, "select[formcontrolname='roles']")
        roles = user_obj['roles'].split(',')
        self.web_elements.choices_items_in_dropdown(dropdown_control=select_element,choice_items=roles)
        div_element = self.find_element(By.CSS_SELECTOR, "div.modal-body.d-flex.gap-3.justify-content-end")
        button = self.find_element(By.XPATH, "//button[text()='Confirm']")
        self.driver.execute_script("arguments[0].click();", button)










        return ret









