import time
from selenium.webdriver.common.by import By
from .base import ApplicationBasePage


class GooglePage(ApplicationBasePage):
    _search_box = (By.XPATH, ".//div[@id='searchform']/descendant::input"
                             "[@aria-label='Buscar']")
    _search_button = (By.XPATH, ".//button[@type='submit']")

    def search(self, search_word):
        self.driver_facade.send_keys(self._search_box, search_word)
        self.driver_facade.click(self._search_button)

    def is_search_correct(self, word):
        title = word + ' - Buscar con Google'
        time.sleep(2)
        return title == self.page_title()
