import json
import os
import time
import re
import xmltodict
from functools import partial
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

class AppNotFoundError(Exception):
    pass


class LoginFailedError(Exception):
    pass


class Driver(webdriver.Remote):

    TIMEOUT = 30
    pausetime = 5  # time in seconds to pause after certain actions

    @classmethod
    def from_config(cls, appname):
        """
        Instanstiate from config file
        """
        conf = loadresource('config')
        desired_capabilities = conf['desired_capabilities']
        if appname in conf['apps']:
            desired_capabilities.update(conf['apps'][appname])
        else:
            raise AppNotFoundError(
                "{appname} not found in config file".format(appname=appname)
                )
        kwargs = {
            'desired_capabilities': desired_capabilities,
            'command_executor': conf['url'],
        }
        return cls(**kwargs)

    def waitnotnone(self, action, retries=5):
        for _ in range(retries):
            result = action()
            if result is not None:
                return result
            self.pause()

    def new_action(self):
        """
        Creates a new TouchAction object with self as context
        """
        return webdriver.common.touch_action.TouchAction(self)

    def tap_element_by_id(self, id):
        """
        Tap element with given id
        """
        self.new_action().tap(
            self.find_element_by_id(id)
        ).perform()

    def set_element_value_by_id(self, id, value):
        """
        Set the value of an element from it's id
        """
        self.set_value(self.find_element_by_id(id), value)
    
    def navigate_to(self, activity, menu_text, menu_icon="menu_icon"):
        """
        navigate to use for navigate to spacific menu

        menu_icon: str | menu button that will show the side menu list

        activity: str | the activity to wait for after the page has been
        selected.
        
        menu_text: str | the text of the button widget in the menu list
        that will be selected.

        """
        self.tap_element_by_id(menu_icon)
        menu_items = self.find_elements_by_class_name("android.widget.Button")
        menu_list = list(map(lambda i: i.get_attribute('text'), menu_items))
        for menu_item in menu_items:
            if menu_list.__contains__(menu_text):
                if menu_item.get_attribute('text') == menu_text:
                    action = self.new_action()
                    action.tap(menu_item)
                    action.perform()
                    time.sleep(5)
                    if activity in self.current_activity:
                        break
                    else:
                        raise AppNotFoundError('{} in not a current activity'.format(activity))
                else:
                    pass
            else:
                raise AppNotFoundError('{} is not exist in menu list'.format(menu_text))
    
    def navigate(self, page, activity=None, menuicon='menu_icon'):
        """
        Navigate uses the menu button to switch pages.

        page: str | the text of the button widget in the menu list
        that will be selected.

        activity: str | the activity to wait for after the page has been
        selected.
        """
        self.tap_element_by_id(menuicon)
        self.pause()
        self.tap_element_by_text(page)

        self.wait_activity(activity, timeout=self.TIMEOUT)

    def get_page(self):
        """
        Get the current page source as a dictionary
        """
        get_page = partial(xmltodict.parse, self.page_source)
        return self.waitnotnone(get_page)

    def find_element_bounds_by_text(self, text):
        """
        Returns the bounds of the first element found to contain the text.
        """

        def parse(data=None):
            data = data if data is not None else self.get_page()
            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, str) and k == '@text' and text in v:
                        return parse_bounds(data['@bounds'])
                    else:
                        d = parse(v)
                        if d is not None:
                            return d
            if isinstance(data, list):
                for d in data:
                    d = parse(d)
                    if d is not None:
                        return d

        def parse_bounds(rawbound):
            rawbound = re.findall(r'\d+', rawbound)
            rawbound = zip(rawbound[::2], rawbound[1::2])
            bound = [(int(x), int(y)) for x, y in rawbound]
            return bound[0]

        return self.waitnotnone(parse)

    def tap_element_by_text(self, text):
        bounds = self.find_element_bounds_by_text(text)
        if bounds is not None:
            x, y = bounds
            self.new_action().tap(x=x, y=y).perform()

    def pause(self):
        time.sleep(self.pausetime)


path, file = os.path.split(os.path.abspath(__file__))


def loadresource(name):
    """
    loads the given file(s) out of resources folder
    """
    filename = '{resourcefolder}/{name}.json'.format(
        resourcefolder=path,
        name=name
        )
    with open(filename) as file:
        return json.load(file)


def saveresource(values, name):
    """
    Saves the `values` to the resource file
    """
    data = loadresource(name)
    data.update(**values)
    filename = '{resourcefolder}/{name}.json'.format(
        resourcefolder=path,
        name=name
        )
    with open(filename, 'w+') as file:
        return json.dump(data, file, indent=4)


class AppiumTest:
    """
    """
    cred = loadresource('config')['cred']

    def __init__(self, appname,useremail=None,password=None):
        self.appname = appname
        self.useremail = useremail or self.cred['user']
        self.password = password or self.cred['pass']
        self.invalid_login_attempt_error = None

        self.driver = Driver.from_config(self.appname)
        self.driver.implicitly_wait(self.driver.TIMEOUT)

    def teardown(self):
        self.driver.quit()
    
    def login_validation(self, curtain="curtain_text"):
        print("login validation function")
        self.driver.tap_element_by_id('buttonLogin')
        self.driver.tap_element_by_id('buttonLogin')
        invalid_login_attempt_error = self.driver.find_element_by_id(curtain).get_attribute('text')
        self.invalid_login_attempt_error = invalid_login_attempt_error

    def login(self):
        self.driver.tap_element_by_id('buttonLogin')
        self.driver.set_element_value_by_id('fieldUser', self.useremail)
        self.driver.set_element_value_by_id('fieldPass', self.password)
        for attempt in range(5):
            if 'Login' in self.driver.current_activity:
                if self.driver.is_keyboard_shown():
                    self.driver.hide_keyboard()
                self.driver.tap_element_by_id("buttonLogin")
                time.sleep(10)
            else:
                break
            if attempt == 4:
                raise LoginFailedError("Could not log into app")

                   
    def assert_elements_exist(self, elements):
        for el in elements:
            try:
                assert bool(self.driver.find_element_by_id(el))
            except Exception as e:
                raise e('{}'.format(el))


    def assert_item_exist(self,element):
        try:
            assert bool(self.driver.find_element_by_id(element))
        except Exception as e:
            raise e('{}'.format(element))

    def click_item_by_id(self,element):
        self.driver.tap_element_by_id(element)

    def sleep_for_some_time(self,time):
        time.sleep(time)

    def __enter__(self):
        self.setup()
        self.login()
        return self

    def __exit__(self, *args, **kwargs):
        self.teardown()
