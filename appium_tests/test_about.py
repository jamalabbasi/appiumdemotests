from .appdriver import AppiumTest, Driver, loadresource
from unittest import TestCase
import time

class TestStartUp(TestCase):

    def setUp(self):
        self.app=AppiumTest('Snapshot','snapshotprodoo@gmail.com','123456')    

    def test_about_tab(self):
        self.app.login()
        self.app.assert_item_exist('aboutTab')
        
    def test_about(self):
        self.app.login()
        self.app.driver.tap_element_by_id('aboutTab')
        try:
            self.app.assert_item_exist('recyclerView') 
        except Exception as e:
            self.app.assert_item_exist('empty_view') 
    
    def test_about_detail(self):
        self.app.login()
        self.app.driver.tap_element_by_id('aboutTab')
        self.app.assert_item_exist('recyclerView')
        time.sleep(5)
        self.app.driver.tap_element_by_id('app_setting_key')
        time.sleep(5)
        self.app.assert_item_exist('txtContent')
    
    def tearDown(self):
        self.app.teardown()
