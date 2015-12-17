from modules.driver import WebDriverFacade


class PageObject(object):

    def __init__(self, driver):
        self.driver_facade = WebDriverFacade(driver)

    @property
    def driver(self):
        return self.driver_facade.driver

    @staticmethod
    def create(page_object_type, **kwargs):
        return PageObjectFactory().create(page_object_type, **kwargs)


class BasePage(PageObject):
    """Base class abstraction that represents a web page"""

    @property
    def page_url(self):
        raise ValueError("You must define an URL for this page")

    def is_text_visible_in_body(self, text):
        """
        Checks whether the given text is present in the html body element of
        this page

        """
        return self.driver_facade.is_text_visible(text)

    def open(self):
        """Opens the page and validates it"""
        self.driver_facade.open(self.page_url)

    def page_title(self):
        """Returns the page title from Selenium.

        This is different from _page_title,
        which is defined for a specific page object and is the expected
        title of the page.

        """
        return self.driver_facade.get_current_page_title_when_available(30)

    def take_screenshot(self, filepath):
        self.driver_facade.take_screenshot(filepath)


class ApplicationBasePage(BasePage):
    """
    Base class abstraction for an application's web page whose URL shares the
    same domain

    Domain: http://www.common-domain.com

    Pages URL: http://www.common-domain.com/pageA
               http://www.common-domain.com/pageB
    """

    def __init__(self, driver, base_url):
        self.driver_facade = WebDriverFacade(driver)
        self.base_url = base_url

    @property
    def page_url(self):
        return self.base_url


class PageObjectFactory(object):

    _singleton = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(PageObjectFactory, cls).__new__(cls, *args,
                                                                   **kwargs)
        return cls._singleton

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    def create(self, page_object_type, **kwargs):
        if issubclass(page_object_type, ApplicationBasePage):
            kwargs["base_url"] = self._base_url
        return page_object_type(self._driver, **kwargs)
