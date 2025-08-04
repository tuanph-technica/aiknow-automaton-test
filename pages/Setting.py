from selenium.webdriver.common.by import By
import time
from base.base_driver import BaseDriver
from pages.Documents import Documents
from pages.setting.ChatPage import ChatPage
from utilities.web_element import WebItem
class Setting(BaseDriver):
    APP_SIDEBAR_MENU_LAYOUT_TAG = "app-sidebar-menu-layout"

    def __init__(self,driver):
        super().__init__(driver)
        self.web_elements = WebItem(driver)
    def get_menu_by_name(self,menu_name="User Management"):
        app_sidebar_layout = self.find_element(By.TAG_NAME,self.APP_SIDEBAR_MENU_LAYOUT_TAG)
        links = app_sidebar_layout.find_elements(By.TAG_NAME,"a")
        for link in links:
            if link.accessible_name == menu_name:
                link.click()
                break
    def get_chat_menu(self):
        self.get_menu_by_name("Chat")
        chat_window = ChatPage(driver=self.driver)
        return chat_window
    def get_documents_menu(self):
        self.get_menu_by_name("Documents")
        document_page = Documents(self.driver)
        return document_page


