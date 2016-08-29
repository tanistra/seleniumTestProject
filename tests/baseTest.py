import unittest

from lib.createDriver import create_driver
from lib.logger import whoami, Logger
from lib.driverCommands import DriverCommands
from lib.configurationReader import load_configuration_from_file


class BaseTest(unittest.TestCase, Logger):
    driver = None
    CONFIG = load_configuration_from_file('connect_config.json')

    @classmethod
    def setUpClass(cls):
        cls.logger('INFO', 'New test suite start')
        cls.driver = create_driver()

    def setUp(self):
        self.testResult = False
        whoami()
        # LOGIN OR SOMETHING SIMILAR

    def tearDown(self):
        whoami()
        if not self.testResult:
            name = self.__class__.id(self).split('.')[3]
            DriverCommands(self.driver).get_screenshot_file(self.driver, name)
            # LOGOUT OR SOMETHING SIMILAR

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.logger('INFO', 'Test suite finished')
