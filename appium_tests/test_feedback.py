from .appdriver import AppiumTest, Driver, loadresource
from unittest import TestCase
from appium.webdriver.common.touch_action import TouchAction

import time

class TestStartUp(TestCase):
    def setUp(self):
        self.app=AppiumTest('Snapshot','snapshotprodoo@gmail.com','123456')    

    def test_feedback_tab(self):
        self.app.login()
        self.app.assert_item_exist('feedbackTab')
    
    def test_feedback(self):
        self.app.login()
        self.app.driver.tap_element_by_id('feedbackTab')
        self.app.assert_item_exist('Description')
    
    def test_discard_feedback(self):
        self.app.login()
        self.app.driver.tap_element_by_id('feedbackTab')
        self.app.assert_item_exist('Description')
        self.app.driver.tap_element_by_id('Discard_Button')
        time.sleep(5)
        self.app.assert_item_exist('feedbackTab')

    def test_save_feedback(self):
        self.app.login()
        self.app.driver.tap_element_by_id('feedbackTab')
        self.app.assert_item_exist('Description')
        self.app.driver.tap_element_by_id('topic')
        self.app.driver.set_element_value_by_id('topic','Test Topic')
        time.sleep(3)
        self.app.driver.tap_element_by_id('Description')
        self.app.driver.set_element_value_by_id('Description', 'This is the description of above topic')
        time.sleep(3)
        self.app.driver.tap_element_by_id('Save_Button')
        time.sleep(15)
        try:   
            self.app.assert_item_exist('feedbackTab')
        except:
            self.app.assert_item_exist('Description')
    def tearDown(self):
        self.app.teardown()