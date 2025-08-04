import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from io import BytesIO
from openpyxl.drawing.image import Image as OpenpyxlImage
class BaseDriver:
    def __init__(self,driver):
        self.driver = driver
    def page_scroll(self):
        pageLength = self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight);var pageLength = document.body.scrollHeight;return pageLength"
        )
        match = False
        while (match == False):
            lastCount = pageLength
            time.sleep(3)
            pageLength = self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight);var pageLength = document.body.scrollHeight;return pageLength"
        )
        if lastCount == pageLength:
            match = True
        time.sleep(4)
    def wait_for_presence_of_all_elements(self,locator_type,locator):
        wait = WebDriverWait(self.driver,10)
        list_elements = wait.until(EC.presence_of_all_elements_located((locator_type,locator)))
        return list_elements
    def wait_until_element_is_clickable(self,locator_type,locator):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable((locator_type,locator)))
        return element
    def find_element(self,locator_type,locator):
        time.sleep(2)
        return self.driver.find_element(locator_type,locator)
    def find_elements_from_node(self,parent_node,locator_type,locator):
        time.sleep(2)
        return parent_node.find_elements(locator_type,locator)
    def find_elements(self,locator_type,locator):
        time.sleep(1)
        return self.driver.find_elements(locator_type,locator)
    def get_dropdown_index_from_string(self,items,value):
        index = 0
        for item in items:
            div_element = item.find_element(By.CLASS_NAME,"ant-select-item-option-content")
            if div_element.text.find(value) >= 0:
                break
            index = index+1
        return index
    def take_screenshot(self):
        screenshot_bytes = self.driver.get_screenshot_as_png()
        return screenshot_bytes












