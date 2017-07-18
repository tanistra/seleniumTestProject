from selenium.webdriver.support.events import AbstractEventListener
from lib.driverCommands import DriverCommands


class Listerers(AbstractEventListener):
    def __init__(self, test_class):
        self.test_class = test_class

    def on_exception(self, exception, driver):
        name = self.test_class['_testMethodName']
        DriverCommands(driver).get_screenshot_file(driver, name)
