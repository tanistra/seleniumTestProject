import os
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchWindowException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from lib.logger import Logger
from lib.waitCommands import WaitCommands
from .configurationReader import load_configuration_from_file

CONFIG = load_configuration_from_file('connect_config.json')


class DriverCommands:
    def __init__(self, driver):
        self.driver = driver
        self.log = Logger()
        self.base_url = CONFIG['BASE_URL']
        self.waitCommands = WaitCommands(self.driver)

    def open_url(self, url):
        self.driver.get(url)
        self.log.logger('INFO', 'Opened url: %s' % url)

    def find_element(self, selector):
        """Find element on application view.

            :param selector: tuple (eg. By.ID, 'element/id')
            :return: elements handler
        """
        try:
            element = self.waitCommands.wait_for_presence_of_element_located(*selector)
        except StaleElementReferenceException:
            self.log.logger('WARNING', 'DOM Exception')
            self.waitCommands.wait(1)
            element = self.driver.wait_for_presence_of_element_located(*selector)
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
        element = self.waitCommands.wait_from_element_clickable(selector, 2)
        element.click()

    def fill_in(self, selector, value, confirm=False):
        """Find element and enter text to the field

            :param selector: tuple (eg. By.ID, 'element/id')
            :param value: text
            :param confirm: if True field is confirmed by send keyboard button Enter
        """
        element = self.waitCommands.wait_for_element_not_visibility(selector)
        element.clear()
        element.send_keys(value)
        if confirm:
            element.submit()

    def move_to_element(self, selector):
        """
        move mouse coursor up to element
        :param selector: selector for element"""
        element = self.find_element(selector)
        ActionChains(self.driver).move_to_element(element).perform()

    def check_page_title(self, expected_title, wait=5):
        """Wait some time until title will be equal to expected

            :param expected_title: expected title to compare
            :param wait: time to wait
        """
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
