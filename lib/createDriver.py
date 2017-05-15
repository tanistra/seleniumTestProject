from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lib.configurationReader import load_configuration_from_file
from lib.logger import Logger

CONFIG = load_configuration_from_file('connect_config.json')

log = Logger()


def create_driver(browser=CONFIG["BROWSER"]):
    """
    Function creates selenium webdriver
    :param browser: specify web browser. Can be:
    * "FF" for firefox browser
    * "CHROME" for chrome,
    * "OPERA" for opera browser
    * "IE" for internet explorer
    * "EDGE" for edge browser
    * "SAFARI" for safari browser
    Default browser is load from config.json file
    :return: driver
    """
    if browser.upper() == "FF":
        d = DesiredCapabilities.FIREFOX
        d['loggingPrefs'] = {'browser': 'ALL'}
        fp = webdriver.FirefoxProfile()
        fp.set_preference('webdriver.log.file', '/tmp/firefox_console')
        driver = webdriver.Firefox(capabilities=d, firefox_profile=fp)
        driver.maximize_window()
    elif browser.upper() == "CHROME":
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'browser': 'ALL'}
        driver = webdriver.Chrome(desired_capabilities=d)
        driver.set_window_size('1680', '1050')
        driver.maximize_window()
    elif browser.upper() == "OPERA":
        driver = webdriver.Opera()
    elif browser.upper() == "IE":
        driver = webdriver.Ie()
        driver.maximize_window()
    elif browser.upper() == "EDGE":
        driver = webdriver.Edge()
    elif browser.upper() == "SAFARI":
        driver = webdriver.Safari()
    else:
        assert False, """
        ERROR! Please check browser in config.json file. BROWSER should = 'FF',
        'CHROME', 'OPERA' 'IE', 'EDGE' or 'SAFARI'
        """

    log.logger('INFO', '%s selenium driver started' % browser)
    return driver
