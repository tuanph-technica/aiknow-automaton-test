import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from pages.homepage import AiKnowHomePage
from utilities.web_element import WebItem


class Login(BaseDriver):
    APP_LOGIN_TAG = "app-login"
    APP_FORGOT_PASSWORD_TAG = "app-forgot-password"
    BUTTON_LOGIN_CLASSNAME = "btn btn-primary"
    TOAST_CONTAINER_ID = "toast-container"
    def __init__(self,driver):
        super().__init__(driver)
        self.web_elements = WebItem(driver)
    def do_login(self,user_name,pass_word):
        app_login = self.find_element(By.TAG_NAME,self.APP_LOGIN_TAG)
        form_groups = app_login.find_elements(By.CLASS_NAME,"form-group")
        txt_user_name = form_groups[0].find_element(By.TAG_NAME,"input")
        txt_pass = form_groups[1].find_element(By.TAG_NAME,"input")
        login_button = app_login.find_element(By.XPATH, "//button[@type='submit']")
        # fill username and password
        self.web_elements.enter_web_item_text(txt_user_name,user_name)
        self.web_elements.enter_web_item_text(txt_pass,pass_word)
        login_button.click()
        try :
            error_container = self.find_element(By.ID,self.TOAST_CONTAINER_ID)
            first_child = error_container.find_element(By.XPATH, "./*[1]")
            err = first_child.text
        except:
            err = ""
        # click login button
        home_page = AiKnowHomePage(self.driver)
        return home_page,err
    def do_forgot_pass_word(self,email):
        app_login = self.find_element(By.TAG_NAME, self.APP_LOGIN_TAG)
        forgot_password_link = app_login.find_element(By.TAG_NAME,"a")
        forgot_password_link.click()
        app_forgot_pass = self.find_element(By.TAG_NAME, self.APP_FORGOT_PASSWORD_TAG)
        input_email = app_forgot_pass.find_element(By.TAG_NAME,"input")
        self.web_elements.enter_web_item_text(input_email,email)
        button_submit = app_forgot_pass.find_element(By.XPATH, "//input[@type='submit']")
        button_submit.click()
        time.sleep(2)
        try :
            error_container = self.find_element(By.ID,self.TOAST_CONTAINER_ID)
            first_child = error_container.find_element(By.XPATH, "./*[1]")
            err = first_child.text
        except:
            err = ""
        if err == "":
            return_value = "ok"
        else:
            return_value = "nok"
        return return_value,err















