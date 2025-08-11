from selenium.webdriver.common.by import By
import time
from base.base_driver import BaseDriver
from pages.Setting import Setting
from pages.UserManagement import UserManagement
from utilities.web_element import WebItem


class AiKnowHomePage(BaseDriver):
    SUB_MENU_LAYOUT_TAG_NAME = "app-sub-menu-layout"
    APP_ADMIN_LAYOUT_TAG = "app-admin-layout"
    MAIN_MENU_LAYOUT_TAG = "app-sidebar-menu-layout"
    def __init__(self,driver):
        super().__init__(driver)
        self.web_elements = WebItem(driver)
    def check_login_success(self):
        try:
            admin_layout = self.find_element(By.TAG_NAME,self.APP_ADMIN_LAYOUT_TAG)
            return "success"
        except:
            return "fail"
    def do_logout(self):
        sub_menu = self.find_element(By.TAG_NAME,self.SUB_MENU_LAYOUT_TAG_NAME)
        li = sub_menu.find_elements(By.TAG_NAME,"li")
        li[2].click()
    def get_menu_by_name(self,menu_name=""):
        side_menu = self.find_element(By.TAG_NAME,self.MAIN_MENU_LAYOUT_TAG)
        menus = side_menu.find_elements(By.TAG_NAME,"a")
        for menu in menus:
            if menu.accessible_name == menu_name:
                menu.click()
                break
    def get_setting_menu(self):
        self.get_menu_by_name(menu_name="Settings")
        setting = Setting(self.driver)
        return setting
    def get_document_menu(self):
        self.get_menu_by_name(menu_name="Documents")
    def get_user_management_menu(self):
        self.get_menu_by_name(menu_name="User Management")
        ret = UserManagement(self.driver)
        return ret



