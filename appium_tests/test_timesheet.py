from .appdriver import AppiumTest, Driver, loadresource
from unittest import TestCase
import time

class TestStartUp(TestCase):

    def setUp(self):
        self.app = AppiumTest('Snapshot','snapshotprodoo@gmail.com','123456')
    
    def test_Timesheet_dashboardtab(self):
        self.app.login()
        self.app.assert_item_exist('timeSheetTab')
    
    def test_timesheet(self):
        self.app.login()
        self.app.driver.tap_element_by_id('timeSheetTab')
        time.sleep(3)
        self.app.assert_item_exist('weekPicker')

    def test_timesheet_approve(self):
        self.app.login()
        self.app.driver.tap_element_by_id('timeSheetTab')
        time.sleep(3)
        self.app.assert_item_exist('weekPicker')
        time.sleep(5)
    
    def test_timesheet_prevoious_week_check(self):
        self.app.login()
        self.app.driver.tap_element_by_id('timeSheetTab')
        time.sleep(3)
        self.app.assert_item_exist('weekPicker')
        time.sleep(10)
        currentWeek = self.app.driver.find_element_by_id('weekPicker')
        text = currentWeek.text
        self.app.driver.tap_element_by_id('backBtn')
        previousWeek=self.app.driver.find_element_by_id('weekPicker')
        text1= previousWeek.text
        if text.__contains__(text1):
            if text.get_attribute('text') != text1:
                time.sleep(5)

    def test_timesheet_next_week_check(self):
        self.app.login()
        self.app.driver.tap_element_by_id('timeSheetTab')
        time.sleep(3)
        self.app.assert_item_exist('weekPicker')
        time.sleep(10)
        currentWeek = self.app.driver.find_element_by_id('weekPicker')
        text = currentWeek.text
        self.app.driver.tap_element_by_id('forwardBtn')
        nextWeek=self.app.driver.find_element_by_id('weekPicker')
        text1= nextWeek.text
        if text.__contains__(text1):
            if text.get_attribute('text') != text1:
                time.sleep(5)
        
    def tearDown(self):
        self.app.teardown()