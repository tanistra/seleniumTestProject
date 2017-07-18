
from lib.createDriver import create_driver
from lib.logger import whoami, Logger
from lib.configurationReader import load_configuration_from_file
from lib.listeners import Listerers
from selenium.webdriver.support.events import EventFiringWebDriver

import unittest


class BaseTest(unittest.TestCase, Logger):
    driver = None
    CONFIG = load_configuration_from_file('connect_config.json')

    @classmethod
    def setUpClass(cls):
        cls.logger('INFO', 'New test suite start')
        cls.driver = create_driver()

    def setUp(self):
        whoami()
        self.driver = EventFiringWebDriver(self.driver, Listerers(self.__dict__))
        # LOGIN OR SOMETHING SIMILAR

    def tearDown(self):
        whoami()
        # LOGOUT OR SOMETHING SIMILAR

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        cls.logger('INFO', 'Test suite finished')
