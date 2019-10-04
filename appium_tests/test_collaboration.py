from .appdriver import AppiumTest, Driver, loadresource
from unittest import TestCase
import time


class TestStartUp(TestCase):
    def setUp(self):
        self.app = AppiumTest('Snapshot','snapshotprodoo@gmail.com','123456')

    def test_collaboration_dashboardtab(self):
        self.app.login()
        self.app.assert_item_exist('collabTab')
    
    def test_collaboration(self):
        self.app.login()
        self.app.assert_item_exist('collabTab')
        self.app.driver.tap_element_by_id('collabTab')
        time.sleep(10)
        self.app.assert_item_exist('collabListItem')


    def tearDown(self): 
        self.app.teardown()