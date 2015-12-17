import time
from selenium.webdriver.common.by import By
from .base import ApplicationBasePage


class GooglePage(ApplicationBasePage):
    _search_box = (By.CSS_SELECTOR, "#sb_ifc0")
    _search_button = (By.CSS_SELECTOR, ".lsb")

    def search(self, search_word):
        self.driver_facade.send_keys(self._search_box, search_word)
        self.driver_facade.click(self._search_button)

    def is_search_correct(self, word):
        title = word + ' - Buscar con Google'
        time.sleep(2)
        return title == self.page_title()
