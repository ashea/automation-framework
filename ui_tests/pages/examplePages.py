from selenium.webdriver.common.by import By
from .base import ApplicationBasePage


class LoginPage(ApplicationBasePage):
    email_input = (By.XPATH, ".//div[@class='login-form']//input[@type='email']")
    password_input = (By.XPATH, ".//div[@class='login-form']//input[@type='password']")
    search_button = (By.XPATH, ".//button[text()='Login']")
    incorrect_credentials_error = (By.XPATH,
                                   ".//div[@class='login-form']//p[text()='Your email or password is incorrect!']")
    login_success_message = (By.XPATH,
                             ".//div[@class='login-form']//p[text()='Login Success!']")

    def input_credentials(self, email, password):
        self.driver_facade.send_keys(self.email_input, email)
        self.driver_facade.send_keys(self.password_input, password)
        self.driver_facade.click(self.search_button)

    def is_login_success(self):
        return self.driver_facade._get_element(self.login_success_message)

    def is_login_error_displayed(self):
        return self.driver_facade._get_element(self.incorrect_credentials_error)
