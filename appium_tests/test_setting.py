from appdriver import AppiumTest, Driver, loadresource
from unittest import TestCase
import time

class TestStartUp(TestCase):

    def setUp(self):
        self.app = AppiumTest('Snapshot','snapshotprodoo@gmail.com','123456')

    def test_settings(self):
        self.app.login()
        self.app.driver.tap_element_by_id('settingTab')
        self.app.assert_item_exist('Heading')

    def test_settings_switchclick(self):
        self.app.login()
        self.app.driver.tap_element_by_id('settingTab')
        self.app.assert_item_exist('Heading')
        self.app.driver.tap_element_by_id('toggBtn')
        self.app.driver.back()
        self.app.driver.tap_element_by_id('settingTab')
        time.sleep(5)
        self.app.assert_item_exist('Heading')
    
    def tearDown(self):
        self.app.teardown()
  