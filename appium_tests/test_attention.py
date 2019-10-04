from appdriver import AppiumTest, Driver, loadresource
from unittest import TestCase
import time

class TestStartUp(TestCase):

    def setUp(self):
        self.app = AppiumTest('Snapshot','snapshotprodoo@gmail.com','123456')
    
    def test_attention_tab(self):
        self.app.login()
        self.app.assert_item_exist('trackerTab')
    
    def test_attention(self):
        self.app.login()
        self.app.driver.tap_element_by_id('trackerTab')
        assert 'AttentionActivity' in self.app.driver.current_activity


    def test_attention_sidemenu(self):
        self.app.login()
        self.app.assert_item_exist('trackerTab')
        self.app.driver.tap_element_by_id('menu_icon')
        self.app.driver.navigate_to('AttentionActivity', 'Attentions')
        time.sleep(10)
        assert 'AttentionActivity' in self.app.driver.current_activity

    def tearDown(self):
        self.app.teardown()