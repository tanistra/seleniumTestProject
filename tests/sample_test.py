from tests.baseTest import BaseTest
from lib.logger import whoami
from lib.driverCommands import DriverCommands
from selenium.webdriver.common.by import By


class SampleTest(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

    def test_01_add(self):
        whoami()
        self.logger('INFO', 'Use logger')

        el = ((By.CSS_SELECTOR, "div.that-does-not-exist"))
        DriverCommands(self.driver).open_url("http://www.google.com")
        DriverCommands(self.driver).find_element(el)

    def test_02_remove(self):
        whoami()
        assert True
        self.testResult = True

