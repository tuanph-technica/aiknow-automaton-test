import os
from datetime import datetime

import pyautogui
import pyperclip
from selenium.webdriver.common.by import By

import time
from base.base_driver import BaseDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.FileUploader import FileUploader
from utilities.ValidationControls import ValidationControls
from utilities.utils import Utils
from utilities.web_element import WebItem
class Documents(BaseDriver):
    def __init__(self,driver):
        super().__init__(driver)
        self.ut = Utils()
        self.web_elements = WebItem(driver)
    def open_select_file_dialog(self,file_path):
        try :
            absolute_file_path = os.path.abspath(file_path)
            upload_div = WebDriverWait(self.driver,10).until(
                EC.element_to_be_clickable((By.TAG_NAME,"app-document-upload-zone"))
            )
            upload_div.click()
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(2)
            pyperclip.copy(absolute_file_path)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Enhanced dialog method failed: {e}")
            return False
    def process_upload_file(self,category_name):
        upload_div = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-document-upload-zone"))
        )
        a_link = upload_div.find_element(By.TAG_NAME,"a")
        a_link.click()
        dropdowns = upload_div.find_elements(By.TAG_NAME,"select")
        time.sleep(2)
        dropdowns[0].click()
        options = dropdowns[0].find_elements(By.TAG_NAME,"option")
        time.sleep(1)
        for option in options:
            if option.text == category_name:
                option.click()
                break
        button = upload_div.find_element(By.TAG_NAME,"button")

        button.click()




