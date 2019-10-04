from .appdriver import AppiumTest, Driver, loadresource
from unittest import TestCase
import time

class TestStartUp(TestCase):

    def setUp(self):
        self.app = AppiumTest('Snapshot','snapshotprodoo@gmail.com','123456')

    def test_login(self):
        self.app.login()
        assert 'DashboardActivity' in self.app.driver.current_activity
    
    def tearDown(self):
        self.app.teardown()
  