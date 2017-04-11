from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement

from after_hooks import AfterHooks
from .container import Container
from .cookies import Cookies
from .exception import NoMatchingWindowFoundException, Error
from .has_window import HasWindow
from .wait.wait import Waitable

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class Browser(Container, HasWindow, Waitable):
    def __init__(self, browser='chrome', *args, **kwargs):
        """
        Creates a watir_snake.browser.Browser instance
        :param browser: firefox, ie, chrome, remote or Selenium WebDriver instance
        :type browser: selenium.webdriver.remote.webdriver.WebDriver or str
        :param args: args passed to the underlying driver
        :param kwargs: kwargs passed to the underlying driver
        """
        if type(browser) == str:
            self.driver = getattr(webdriver, browser.capitalize())(*args, **kwargs)
        elif isinstance(browser, webdriver.Remote):
            self.driver = browser
        else:
            raise TypeError('A WebDriver instance must be supplied')

        self.after_hooks = AfterHooks(self)
        self.current_frame = None
        self.closed = False

    @property
    def wd(self):
        return self.driver

    @staticmethod
    def start(url, browser='chrome', *args, **kwargs):
        """
        Creates a Browser instance
        :param url: url to navigate to after starting browser
        :type url: str
        :param browser: firefox, ie, chrome, remote or Selenium WebDriver instance
        :type browser: selenium.webdriver.remote.webdriver.WebDriver or str
        :param args: args passed to the underlying driver
        :param kwargs: kwargs passed to the underlying driver
        """
        b = Browser(browser, *args, **kwargs)
        b.goto(url)
        return b

    def __repr__(self):
        try:
            return '#<{}:0x{:x} url={!r} title={!r}>'.format(self.__class__.__name__,
                                                             self.__hash__() * 2, self.url,
                                                             self.title)
        except:
            return '#<{}:0x{:x} closed={}>'.format(self.__class__.__name__, self.__hash__() * 2,
                                                   self.closed)

    selector_string = __repr__

    def goto(self, uri):
        """
        Goes to the given URL
        :param uri: the URL
        :type uri: str
        :return: the url you end up at
        :rtype: str
        """
        if urlparse(uri).scheme == '':
            uri = 'http://{}'.format(uri)

        self.driver.get(uri)
        # self.after_hooks.run  # TODO
        return uri

    def back(self):
        """ Navigates back in history """
        self.driver.back()

    def forward(self):
        """ Navigates forward in history """
        self.driver.forward()

    @property
    def url(self):
        """
        Returns the URL of the current page
        :rtype: str
        """
        # self.assert_exists  # TODO
        return self.driver.current_url

    @property
    def title(self):
        """
        Returns the title of the current page
        :rtype: str
        """
        return self.driver.title

    def close(self):
        """ Closes the browser """
        if not self.closed:
            self.driver.quit()
            self.closed = True

    quit = close

    @property
    def cookies(self):
        """
        Handles cookies
        :rtype: watir_snake.cookies.Cookies
        """
        return Cookies(self.driver)

    @property
    def name(self):
        """
        Returns the browser name
        :rtype: str
        """
        return self.driver.name

    @property
    def text(self):
        """
        Returns the text of the page body
        :return:
        """
        # return self.body.text  # TODO
        return None

    @property
    def html(self):
        """
        Returns HTML code of the current page
        :rtype: str
        """
        return self.driver.page_source

    @property
    def alert(self):
        """
        Handles Javascript alerts, confirms and prompts
        :rtype: watir_snake.alert.Alert
        """
        # return Alert(self)  # TODO
        return None

    def refresh(self):
        """ Refreshes the current page """
        self.driver.refresh()
        # self.after_hooks.run  # TODO

    def wait(self, timeout=5):
        """
        Waits until the readyState of document is complete, raises a TimeoutException if timeout is
        exceeded
        :param timeout: time to wait
        :type timeout: int
        """
        # wait_until(timeout: timeout, message: "waiting for document.readyState == 'complete'") do
        #     ready_state == "complete"
        raise TimeoutException
        return None  # TODO

    @property
    def ready_state(self):
        """
        Returns the readyState of the document
        :rtype: str
        """
        return self.execute_script('return document.readyState;')

    @property
    def status(self):
        """
        Returns the text of the status bar
        :return:
        """
        return self.execute_script('return window.status;')

    def execute_script(self, script, *args):
        """
        Executes JavaScript snippet
        :param script: Javascript Snippet to execute
        :type script: str
        :param args: Arguments will be available in the given script in the 'arguments' pseudo-array
        :return: result of script
        """
        from .elements.element import Element
        args = [e.wd if isinstance(e, Element) else e for e in args]
        returned = self.driver.execute_script(script, *args)

        # return wrap_elements_in(returned)  # TODO
        return returned

    def send_keys(self, *args):
        """
        Sends sequence of keystrokes to currently active element
        :param args: keystrokes
        """
        self.driver.switch_to.active_element.send_keys(*args)

    @property
    def screenshot(self):
        """
        Handles screenshots of current pages
        :rtype: watir_snake.screenshot.Screenshot
        """
        from .screenshot import Screenshot
        return Screenshot(self.driver)

    @property
    def exist(self):
        """
        True if browser is not closed and False otherwise
        :rtype: bool
        """
        try:
            # assert_exists  # TODO
            return True
        except (NoMatchingWindowFoundException, Error):
            return False

    exists = exist

    def assert_exists(self):
        if self.closed:
            raise StandardError('browser was closed')
        # elif not window.present:  # TODO
        #     raise NoSuchWindowException('browser window was closed')
        else:
            self.driver.switch_to.default_content()
            return True

    wait_for_exists = assert_exists
    wait_for_present = assert_exists

    @property
    def browser(self):
        return self

    def wrap_elements_in(self, obj):
        if type(obj) == WebElement:
            return self.wrap_element(obj)
        elif type(obj) == list:
            return [self.wrap_elements_in(e) for e in obj]
        elif type(obj) == dict:
            for k, v in obj.items():
                obj[k] = self.wrap_elements_in(v)
            return obj
        else:
            return obj

    def wrap_element(self, element):
        # Watir.element_class_for(element.tag_name.downcase).new(self, element: element)  # TODO
        return None