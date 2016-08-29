import os
import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from lib.logger import Logger
from .configurationReader import load_configuration_from_file

CONFIG = load_configuration_from_file('connect_config.json')


class DriverCommands:
    def __init__(self, driver):
        self.driver = driver
        self.wait_time = 5
        self.log = Logger()
        self.base_url = CONFIG['BASE_URL']

    def find_element(self, selector):
        """Find element on application view.

            :param selector: tuple (eg. By.ID, 'element/id')
            :return: elements handler
        """
        if len(self.find_elements(selector)) == 0:
            raise AssertionError('Could not locate elements by parameters: %s' % str(selector))
        try:
            element = self.driver.find_element(*selector)
        except StaleElementReferenceException:
            self.log.logger('WARNING', 'DOM Exception')
            element = self.driver.find_element(*selector)
        return element

    def find_elements(self, selector):
        """Find all element on visible view with selector

            :param selector: elements selector
        """
        elements = self.driver.find_elements(*selector)
        return elements

    def scroll_to_bottom(self):
        """scroll to the end of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def is_element_displayed(self, selector):
        """Returns bool value if element is or isn't displayed on page

            :param selector: eg. (By.ID, 'elementID')
            :return: bool
        """
        if len(self.find_elements(selector)) == 0:
            return False
        else:
            element = self.driver.find_element(*selector)
            return element.is_displayed()

    def click_element(self, selector):
        """Find element and click on it.

            :param selector: tuple (eg. By.ID, 'element/id')
        """
        try:
            element = self.wait_from_element_clickable(selector, 2)
            element.click()
        except Exception as e:
            self.log.logger('WARNING', e)
            self.wait(1)
            element = self.find_element(selector)
            element.click()

    def fill_in(self, selector, value, confirm=False):
        """Find element and enter text to the field

            :param selector: tuple (eg. By.ID, 'element/id')
            :param value: text
            :param confirm: if True field is confirmed by send keyboard button Enter
        """
        element = self.wait_for_element_visibility(selector)
        element.clear()
        element.send_keys(value)
        if confirm:
            element.submit()

    def check_page_title(self, expected_title, wait=5):
        """Wait some time until title will be equal to expected

            :param expected_title: expected title to compare
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        try:
            WebDriverWait(self.driver, wait).until(EC.title_is(expected_title))
            self.log.logger('INFO', 'Page title is correct')
        except TimeoutException:
            title = self.get_page_title()
            raise AssertionError('Wrong page title, should be "%s", but is: "%s"' % (expected_title, title))

    def get_page_title(self):
        """Get current page title
        :return: page title
        """
        return self.driver.title

    def check_url(self, expected_url):
        """Check current url

        :param expected_url: expected url to compare with current url
        """
        expected_url = CONFIG['BASE_URL'] + expected_url
        url = self.driver.current_url
        assert url == expected_url, 'Wrong page url expected: "%s", but is: %s' % (expected_url, url)

    def get_text_from_element(self, selector):
        """Find element and get text from it.

            :param selector: tuple (eg. By.ID, 'element/id')
            :return: text from element
        """
        element = self.find_element(selector)
        return element.text

    def get_attribute_from_element(self, selector, attribute='value'):
        """Find element and get text from it.

            :param selector: tuple (eg. By.ID, 'element/id')
            :param attribute: html value
            :return: text from element
        """
        element = self.find_element(selector)
        return element.get_attribute(attribute)

    def check_element_text(self, selector, expected_text, skip_new_line=False):
        """Find element, get text from it and compare with your expectation.

            :param selector: element to get text
            :param expected_text: text to compare with text from element
            :param skip_new_line: set true if you want skip '\\n' sign
        """
        self.log.logger('INFO', 'Checking text. Text should be %s' % expected_text)
        element_text = self.get_text_from_element(selector)
        if skip_new_line:
            element_text = element_text.replace('\n', '')
        assert element_text == expected_text, "Wrong text. Should be '%s' instead of '%s'" % (
            expected_text, element_text)

    def check_element_attribute(self, selector, attribute, expected):
        """Find element, get attribute from it and compare with your expectation.

            :param selector: tuple - element to get attribute
            :param attribute: string - web element attribute e.g ()
            :param expected: text to compare with text from web element attribute
        """
        self.log.logger('INFO', 'Checking text. Text should be %s' % expected)
        attribute_value = self.get_attribute_from_element(selector, attribute)
        assert attribute_value == expected, "Wrong attribute value. Should be '%s' instead of '%s'" % (
            expected, attribute_value)

    def check_checkbox_is_selected(self, selector):
        """Find checkbox and check if it is selected

            :param selector: tuple (eg. By.ID, 'element/id')
            :return: checkbox state (True or False)
        """
        element = self.find_element(selector)
        return element.is_selected()

    # WAIT METHODS

    def wait_for_element_visibility(self, selector, wait=None):
        """Wait some time until expected element will be visible on current page

            :param selector: element selector
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        try:
            element = WebDriverWait(self.driver, wait).until(EC.visibility_of_element_located(selector))
            return element
        except (TimeoutException, NoSuchElementException):
            raise AssertionError('Could not find element' + str(selector))

    def wait_for_js_alert_not_visibility(self, wait=None):
        """ Wait for 5 seconds until connect JavaScript alert missing """
        alert_selector = (By.CSS_SELECTOR, "body > div.notifyjs-corner")
        wait = wait or self.wait_time
        try:
            WebDriverWait(self.driver, wait).until_not(EC.visibility_of_element_located(alert_selector))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_element_not_visibility(self, selector, wait=None):
        """Wait some time until visible element disappear

            :param selector: element selector
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        try:
            WebDriverWait(self.driver, wait).until_not(EC.visibility_of_element_located(selector))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_alert_not_visibility(self, wait=None):
        """ Wait some time until page alert is not visible on page
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        try:
            WebDriverWait(self.driver, wait).until_not(EC.alert_is_present())
        except TimeoutException:
            self.log.logger('INFO', 'Alert still presented')

    def wait_for_presence_of_element_located(self, selector, wait=None):
        """
        Wait some time for element presence in DOM

            :param selector: element to wait for
            :param wait: time to wait
            :return: element
        """
        wait = wait or self.wait_time
        try:
            presence_of_element = WebDriverWait(self.driver, wait).until(
                EC.presence_of_element_located(selector))
            return presence_of_element
        except (TimeoutException, NoSuchElementException):
            raise AssertionError('Timeout, elemenent is not presented')

    def wait_for_expected_text(self, selector, expected_text, wait=None):
        """Wait some time until expected text will be visible on current page

            :param expected_text: expected title to compare
            :param selector: element selector
            :param wait: time to wait
        """
        wait = wait or self.wait_time
        try:
            text_is_present = WebDriverWait(self.driver, wait).until(
                EC.text_to_be_present_in_element(selector, expected_text))
            return text_is_present
        except (TimeoutException, NoSuchElementException):
            raise AssertionError('Something went wrong with reading text from the element' + str(selector))

    def wait_for_alert(self, wait=None):
        """
        Wait some time until for alert presented
        :param wait: time to wait
        :return: Bool
        """
        wait = wait or self.wait_time
        try:
            WebDriverWait(self.driver, wait).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.log.logger('INFO', 'Alert presented with message: %s' % alert.text)
            return True
        except TimeoutException:
            self.log.logger('INFO', 'Any alert presented')
            return False

    def wait_for_alert_accept(self, wait=None):
        """ Wait for alert and accept if presented

        :param wait: time to wait for alert
        """
        wait = wait or self.wait_time
        try:
            WebDriverWait(self.driver, wait).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.log.logger('INFO', 'Alert text: %s\n' % alert.text)
            alert.accept()
            self.log.logger('INFO', "Alert has been accepted")
            return True
        except TimeoutException:
            self.log.logger('WARNING', "No alert shown this time")
            return False

    def wait_from_element_clickable(self, selector, wait=None):
        """ Wait some time for element to be clickable. Clickable means that element is visible and is enabled.

        :param selector: element
        :param wait: time to wait
        :return: element if clickable or assertionError if not
        """
        wait = wait or self.wait_time
        try:
            element = WebDriverWait(self.driver, wait).until(EC.element_to_be_clickable(selector))
            return element
        except TimeoutException as e:
            self.log.logger('ERROR', e)
            raise AssertionError('Element is not clickable')

    def get_screenshot_file(self, driver, file_name):
        """
        Function create screenshot png file in the screenshot directory
        :param driver: webdriver
        :param file_name: name of the screenshot file
        """
        scr_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'screenshots/')
        scr_file = scr_dir + file_name + '.png'
        try:
            driver.get_screenshot_as_file(scr_file)
            self.log.logger('INFO', 'Screenshot saved: %s' % scr_file)
        except NoSuchWindowException:
            print('ERROR: Browser unable to get a screenshot')

    @staticmethod
    def wait(seconds):
        time.sleep(seconds)
