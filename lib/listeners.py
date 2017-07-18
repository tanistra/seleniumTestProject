from selenium.webdriver.support.events import AbstractEventListener
from lib.driverCommands import DriverCommands


class Listerers(AbstractEventListener):

    def on_exception(self, exception, driver):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++")
        print(exception.__dict__)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++")
        # name = self.__class__(self).split('.')[3]
        DriverCommands(driver).get_screenshot_file(driver, "123123")
