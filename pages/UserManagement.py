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
class UserManagement(BaseDriver):
    def __init__(self,driver):
        super().__init__(driver)
        self.ut = Utils()
        self.web_elements = WebItem(driver)
