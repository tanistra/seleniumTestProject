import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from lib.logger import Logger
from .configurationReader import load_configuration_from_file

CONFIG = load_configuration_from_file('connect_config.json')


class WaitCommands:
    def __init__(self, driver):
        self.driver = driver
        self.log = Logger()
        self.wait_time = CONFIG["WAIT_TIMEOUT"]

    def __web_driver_wait(self, driver, wait=None):
        wait = wait or self.wait_time
        return WebDriverWait(driver, wait)

    def wait_for_element_visibility(self, selector, wait=None):
        """Wait some time until expected element will be visible on current page

            :param selector: element selector
            :param wait: time to wait
        """
        try:
            element = self.__web_driver_wait(wait).until(EC.visibility_of_element_located(selector))
            return element
        except (TimeoutException, NoSuchElementException):
            raise AssertionError('Could not find element' + str(selector))

    def wait_for_js_alert_not_visibility(self, wait=None):
        """ Wait for 5 seconds until connect JavaScript alert missing """
        alert_selector = (By.CSS_SELECTOR, "body > div.notifyjs-corner")
        self.__web_driver_wait(wait).until_not(EC.visibility_of_element_located(alert_selector))

    def wait_for_element_not_visibility(self, *selector, wait=None):
        """Wait some time until visible element disappear

            :param selector: element selector
            :param wait: time to wait
        """
        try:
            self.__web_driver_wait(wait).until_not(EC.visibility_of_element_located(selector))
        except (TimeoutException, NoSuchElementException):
            raise AssertionError("Element should not be visible: " + str(selector))

    def wait_for_alert_not_visibility(self, wait=None):
        """ Wait some time until page alert is not visible on page
            :param wait: time to wait
        """
        try:
            self.__web_driver_wait(wait).until_not(EC.alert_is_present())
        except TimeoutException:
            raise AssertionError("Alert still visible")

    def wait_for_presence_of_element_located(self, *selector, wait=None):
        """
        Wait some time for element presence in DOM
            :param selector: element to wait for
            :param wait: time to wait
            :return: element or raise Assertion 
        """
        try:
            return self.__web_driver_wait(self.driver, wait).until(EC.presence_of_element_located(*selector))
        except (TimeoutException, NoSuchElementException):
            raise AssertionError('Timeout, elemenent is not presented')

    def wait_for_expected_text(self, selector, expected_text, wait=None):
        """Wait some time until expected text will be visible on current page

            :param expected_text: expected title to compare
            :param selector: element selector
            :param wait: time to wait
        """
        try:
            return self.__web_driver_wait(wait).until(EC.text_to_be_present_in_element(selector, expected_text))
        except (TimeoutException, NoSuchElementException):
            raise AssertionError('Something went wrong with reading text from the element' + str(selector))

    def wait_for_alert(self, wait=None):
        """
        Wait some time until for alert presented
        :param wait: time to wait
        :return: Bool
        """
        try:
            self.__web_driver_wait(wait).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.log.logger('INFO', 'Alert presented with message: %s' % alert.text)
        except TimeoutException:
            raise AssertionError('Alert not presented')

    def wait_for_alert_accept(self, wait=None):
        """ Wait for alert and accept if presented

        :param wait: time to wait for alert
        """
        try:
            self.__web_driver_wait(wait).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.log.logger('INFO', 'Alert text: %s\n' % alert.text)
            alert.accept()
            self.log.logger('INFO', "Alert has been accepted")
        except TimeoutException:
            self.log.logger('WARNING', "No alert shown this time")
            raise AssertionError('Alert not presented')

    def wait_from_element_clickable(self, selector, wait=None):
        """ Wait some time for element to be clickable. Clickable means that element is visible and is enabled.

        :param selector: element
        :param wait: time to wait
        :return: element if clickable or assertionError if not
        """
        try:
            return self.__web_driver_wait(wait).until(EC.element_to_be_clickable(selector))
        except TimeoutException as e:
            self.log.logger('ERROR', e)
            raise AssertionError('Element is not clickable')

    def wait_for_condition(self, condition):
        self.__web_driver_wait(self.driver).until(lambda x: condition)

    @staticmethod
    def wait(seconds):
        time.sleep(seconds)
