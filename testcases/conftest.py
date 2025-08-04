import pytest
from selenium import webdriver
import seleniumwire
import os
from selenium.webdriver.support.wait import WebDriverWait
from utilities.ExcelUtil import readData
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())

# User accounts for parallel testing
USER_ACCOUNTS = [
    {"username": "auto_user0001", "password": "123456"},
    {"username": "auto_user0002", "password": "123456"},
    {"username": "auto_user0002", "password": "123456"},
    {"username": "auto_user0004", "password": "123456"},
    {"username": "auto_user0005", "password": "123456"},
]

@pytest.fixture(scope="session")
def user_account(worker_id):
    """Assign different user accounts to each worker"""
    if worker_id == "master":
        # When not running in parallel, use first account
        return USER_ACCOUNTS[0]
    
    # Extract worker number and map to account
    worker_num = int(worker_id.replace("gw", ""))
    account_index = worker_num % len(USER_ACCOUNTS)
    return USER_ACCOUNTS[account_index]



class EdgeCromiumDriverManager:
    pass

def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")

@pytest.fixture(scope="class")
def setup(request):
    # for debuging
    ENVIRONMENT_CONFIG_FILE = '..//testdata/car_infomation_testing_jpn.xlsx'

    #ENVIRONMENT_CONFIG_FILE = './/testdata/car_infomation_testing_jpn.xlsx'
    #browser = readData(ENVIRONMENT_CONFIG_FILE,'Sheet2',2,2)
    #url = readData(ENVIRONMENT_CONFIG_FILE,'Sheet2',2,3)
    #role = readData(ENVIRONMENT_CONFIG_FILE,'Sheet2',2,1)
    browser = 'chrome'
    url = "http://aiknow-v2.technica.vn/auth/login"
    headless = request.config.getoption("--headless")
    
    if browser == 'chrome':
        driver_path = os.path.expanduser("~/chromedriver/chromedriver-linux64/chromedriver")
        service = Service(driver_path)
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=service, options=chrome_options)
    elif browser == 'firefox':
        driver = webdriver.Firefox()
    elif browser == 'edge':
        driver = webdriver.Edge()
    else:
        driver = webdriver.Ie()
    driver.get(url=url)
    if not headless:
        driver.maximize_window()
    request.cls.driver = driver
    #request.cls.role = role
    yield
    driver.close()


"""
@pytest.fixture(scope="class")
def setup(request):
    ENVIRONMENT_CONFIG_FILE = './/testdata/car_infomation_testing_jpn.xlsx'
    browser = readData(ENVIRONMENT_CONFIG_FILE,'Sheet2',2,2)
    url = readData(ENVIRONMENT_CONFIG_FILE,'Sheet2',2,3)
    role = readData(ENVIRONMENT_CONFIG_FILE,'Sheet2',2,1)
    if browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser == 'firefox':
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser == 'edge':
        driver = webdriver.Edge(EdgeCromiumDriverManager().install())
    else:
        driver = webdriver.Ie()
    driver.get(url=url)
    driver.maximize_window()
    request.cls.driver = driver
    request.cls.role = role
    yield
    driver.close()
def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--url")
    parser.addoption("--role")
@pytest.fixture(scope="class",autouse=True)
def browser(request):
    return  request.config.getoption("--browser")
@pytest.fixture(scope="class",autouse=True)
def url(request):
    return  request.config.getoption("--url")
@pytest.fixture(scope="class",autouse=True)
def role(request):
    return  request.config.getoption("--role")
"""





