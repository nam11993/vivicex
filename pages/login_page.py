from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class LoginPage(BasePage):
    login_path = "/login"

    def __init__(
        self,
        driver,
        base_url: str,
        timeout: int = 15,
        email_selector: str = "id=email",
        password_selector: str = "id=password",
        submit_selector: str = "css=button[type='submit']",
        error_selector: str = "css=.error,.alert,[role='alert']",
        logged_in_selector: str = "css=[data-testid='user-menu'],.user-menu,.account-menu",
        slow_motion: float = 0.0,
    ) -> None:
        super().__init__(driver, base_url, timeout, slow_motion)
        self.email_input = self.parse_locator(email_selector)
        self.password_input = self.parse_locator(password_selector)
        self.submit_button = self.parse_locator(submit_selector)
        self.error_message = self.parse_locator(error_selector)
        self.logged_in_marker = self.parse_locator(logged_in_selector)

    def open(self) -> None:
        self.open_path(self.login_path)

    def login(self, email: str, password: str) -> None:
        self.type_text(self.email_input, email)
        self.type_text(self.password_input, password)
        self.click(self.submit_button)

    def get_error_message(self) -> str:
        return self.visible_text(self.error_message)

    def is_logged_in(self) -> bool:
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.logged_in_marker)
            )
            return True
        except TimeoutException:
            return False

    def has_error_message(self) -> bool:
        try:
            return bool(self.get_error_message())
        except TimeoutException:
            return False
