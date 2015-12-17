import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.common.exceptions import NoSuchElementException


global_timeout = 0


def _create_firefox_driver(proxy_url, user_agent):
    _proxy = None
    profile = webdriver.FirefoxProfile()
    profile.set_preference("intl.accept_languages", "en-us")
    if user_agent:
        profile.set_preference("general.useragent.override", user_agent)
    if proxy_url:
        _proxy = Proxy({
            'proxyType': 'MANUAL',
            'httpProxy': proxy_url,
            'ftpProxy': proxy_url,
            'sslProxy': proxy_url
        })
    return webdriver.Firefox(firefox_profile=profile, proxy=_proxy)


def _create_chrome_driver(proxy_url):
    chrome_options = None
    if proxy_url:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % proxy_url)

    return webdriver.Chrome(chrome_options=chrome_options)


def create_new_driver(browser_name, proxy_url, timeout, browser_size, user_agent):
    """Main method to create the selenium driver"""
    global global_timeout
    global_timeout = timeout

    if browser_name == 'firefox':
        driver = _create_firefox_driver(proxy_url, user_agent)
    elif browser_name == 'chrome':
        driver = _create_chrome_driver(proxy_url)
    else:
        raise ValueError("The driver couldn't be created")
    driver.maximize_window()
    if browser_size == 'small':
        driver.set_window_size(400, 600)
    elif browser_size == 'medium':
        driver.set_window_size(768, 1024)
    elif browser_size == 'large':
        driver.set_window_size(1280, 1024)

    driver.implicitly_wait(timeout)

    return driver


class WebDriverFacade(object):
    """Facade that encapsulates all the interactions with web driver"""

    def __init__(self, driver):
        self.driver = driver

    def _get_element(self, locator, index=0):
        if index < 0:
            raise ValueError("Index must be a greater than or equals zero")

        elements = self.driver.find_elements(*locator)
        if not elements:
            raise NoSuchElementException(
                "There couldn't be found any elements with the following "
                "selector: %s" % str(locator))
        return elements[index]

    def open(self, url):
        """Opens the page at the given url"""

        self.driver.get(url)

    def click(self, locator, explicit_wait_after_click=None, index=0):
        """Clicks on the element at the given index from locator"""
        self._get_element(locator, index).click()
        if explicit_wait_after_click:
            time.sleep(explicit_wait_after_click)

    def get_current_page_title_when_available(self, timeout):
        """
        Returns the page title from Selenium, the page the current driver is at

        """
        WebDriverWait(self.driver, timeout).until(lambda s: s.title)
        return self.driver.title

    def is_text_visible(self, text):
        """
        Returns true if the specified text is visible in the html body element
        of the page this driver is currently at

        """
        body = self.driver.find_element_by_tag_name("body")
        return text in body.text

    @staticmethod
    def list_files_with_extension(path, extension):
        """
        Returns a list of names of all files with given extension in a folder
        path
        """
        files = []
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)) and name.endswith(
                    extension):
                files.append(name)
        return files

    def send_keys(self, locator, keys):
        """Sends keys to the given locator"""
        self.driver.find_element(*locator).send_keys(keys)

    def take_screenshot(self, filepath):
        self.driver.get_screenshot_as_file(filepath)
