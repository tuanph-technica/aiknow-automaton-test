
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from base.base_driver import BaseDriver
DROPDOWN_CONTENT_LIST_TAG = "cdk-virtual-scroll-viewport"
NZ_OPTION_ITEM = "nz-option-item"
class WebItem(BaseDriver):
    def __init__(self,driver):
        super().__init__(driver)
    def enter_text(self,text_element,text_value):
        time.sleep(1)
        text_element.send_keys(Keys.CONTROL + "a")  # Select all
        text_element.send_keys(Keys.DELETE)  # Delete selected text
        text_element.send_keys(text_value)
        text_element.send_keys(Keys.TAB)
    def enter_web_item_text(self,text_element, text_value):
        time.sleep(1)
        text_element.send_keys(Keys.CONTROL + "a")  # Select all
        text_element.send_keys(Keys.DELETE)  # Delete selected text
        text_element.send_keys(text_value)
        time.sleep(1)
    def press_enter_on_text_control(self,text_element):
        time.sleep(1)
        text_element.send_keys(Keys.ENTER)


    def enter_web_item_drop_down(self,dropdown_element,option_text):
        time.sleep(2)
        dropdown_element.click()
        time.sleep(1)
        dropdown_content = self.find_element(By.TAG_NAME, DROPDOWN_CONTENT_LIST_TAG)
        dropdown_items = self.find_elements_from_node(dropdown_content, By.TAG_NAME,NZ_OPTION_ITEM)
        if isinstance(option_text,int):
            dropdown_items[option_text].click()
        else:
            for item in dropdown_items:
                if item.text == option_text:
                    item.click()
                    break
        time.sleep(1)
    def click_button(self,button):
        self.driver.execute_script("arguments[0].click();", button)
    def double_click_button(self,button):
        actions = ActionChains(self.driver)
        actions.double_click(button).perform()
    def get_table_from_parent(self,parent_control):
        table = parent_control.find_element(By.TAG_NAME,"table")
        return table
    def get_row_from_table(self,table_control,index):
        body = table_control.find_element(By.TAG_NAME,"tbody")
        rows = body.find_elements(By.TAG_NAME,"tr")
        return rows[index]
    def choices_items_in_dropdown(self,dropdown_control=None,choice_items=[]):

        self.driver.execute_script("arguments[0].click();", dropdown_control)
        options = dropdown_control.find_elements(By.TAG_NAME,"option")
        for option in options:
            if option.text in choice_items:
                options.click()












