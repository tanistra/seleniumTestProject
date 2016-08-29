from tests.baseTest import BaseTest
from lib.logger import whoami


class SampleTest(BaseTest):

    def setUp(self):
        BaseTest.setUp(self)

    def test_01_add(self):
        whoami()
        self.logger('INFO', 'Use logger')
        assert True
        self.testResult = True

    def test_02_edit(self):
        whoami()
        assert False
        self.testResult = True

    def test_03_remove(self):
        whoami()
        assert True
        self.testResult = True

