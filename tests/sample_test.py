from tests.baseTest import BaseTest
from lib.logger import whoami
from lib.driverCommands import DriverCommands
from selenium.webdriver.common.by import By
from lib.configurationReader import load_configuration_from_file
import time

CONFIG = load_configuration_from_file("connect_config.json")

MENU = (By.CSS_SELECTOR, "[module='shell.menu.ProductLauncher']")

PROCESS_LIST = (By.CSS_SELECTOR, "Process List")


class SampleTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.browser = DriverCommands(self.driver)

    def test_01_add(self):
        whoami()
        url = CONFIG["BASE_URL"]
        DriverCommands(self.driver).open_url(url)

        self.browser.fill_in((By.ID, "lst-ib"), "dupeczki")

        print(self.browser.get_text_from_element((By.ID, "lst-ib")))

        self.browser.click_by_locator((By.ID, "gbwa"))

        self.browser.waitCommands.wait_for_presence_of_element_located((By.XPATH, './/*[@aria-label="Aplikacje Google"]'))
        print(self.browser.get_text_from_element((By.ID, "gb78")))

        time.sleep(5)
        print("dupczeka")