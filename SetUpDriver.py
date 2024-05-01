from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class SetUpDriver:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options)

        driver.maximize_window()
        self.driver = driver

    def get_driver(self):
        return self.driver