import unittest

from lib.createDriver import create_driver
from lib.logger import whoami, Logger
from lib.driverCommands import DriverCommands
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
        cls.driver = EventFiringWebDriver(create_driver(), Listerers())

    def setUp(self):
        self.testResult = False
        whoami()
        # LOGIN OR SOMETHING SIMILAR

    def tearDown(self):
        whoami()
        # LOGOUT OR SOMETHING SIMILAR

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.logger('INFO', 'Test suite finished')
