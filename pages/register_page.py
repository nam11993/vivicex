from __future__ import annotations

from urllib.parse import urlencode

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class RegisterPage(BasePage):
    title = (By.CSS_SELECTOR, "[data-i18n-key='register.title']")
    email_input = (By.CSS_SELECTOR, "[data-testid='email-text-input']")
    legal_checkbox = (By.CSS_SELECTOR, "[data-testid='legal-acceptance-checkbox']")
    submit_button = (By.CSS_SELECTOR, "[data-testid='submit-button']")
    login_link = (By.CSS_SELECTOR, "a[href*='/loginname']")
    terms_link = (By.CSS_SELECTOR, "a[href*='terms-and-conditions']")
    privacy_link = (By.CSS_SELECTOR, "a[href*='privacy-policy']")
    language_button = (By.CSS_SELECTOR, "button[aria-haspopup='listbox']")
    dark_mode_button = (By.CSS_SELECTOR, "button[aria-label='Switch to dark mode']")

    password_title = (By.CSS_SELECTOR, "h1")
    password_input = (By.CSS_SELECTOR, "[data-testid='password-text-input']")
    password_toggle_button = (By.CSS_SELECTOR, "[data-testid='password-text-input'] + div button")
    back_button = (By.XPATH, "(//input[@data-testid='password-text-input']/ancestor::form/preceding::button)[last()]")
    confirm_back_button = (By.XPATH, "//button[normalize-space()='Yes' or normalize-space()='C\u00f3']")
    password_rule_locators = {
        "length": (By.CSS_SELECTOR, "[data-testid='length-check'] svg"),
        "uppercase": (By.CSS_SELECTOR, "[data-testid='uppercase-check'] svg"),
        "lowercase": (By.CSS_SELECTOR, "[data-testid='lowercase-check'] svg"),
        "number": (By.CSS_SELECTOR, "[data-testid='number-check'] svg"),
        "symbol": (By.CSS_SELECTOR, "[data-testid='symbol-check'] svg"),
    }

    referral_title = (By.CSS_SELECTOR, "h1")
    referral_input = (By.ID, "register-referral-input")
    referral_skip_button = (
        By.XPATH,
        "//input[@id='register-referral-input']/ancestor::form//button"
        "[normalize-space()='Skip' or normalize-space()='B\u1ecf qua']",
    )
    referral_continue_button = (
        By.XPATH,
        "//input[@id='register-referral-input']/ancestor::form//button"
        "[normalize-space()='Continue' or normalize-space()='Ti\u1ebfp t\u1ee5c']",
    )
    otp_input = (By.CSS_SELECTOR, "input[maxlength='6']")
    resend_button = (
        By.XPATH,
        "//button[starts-with(normalize-space(), 'Resend') or starts-with(normalize-space(), 'G\u1eedi l\u1ea1i')]",
    )
    email_verify_next_button = (
        By.XPATH,
        "//button[normalize-space()='Next' or normalize-space()='Ti\u1ebfp theo']",
    )
    email_verify_back_button = (By.XPATH, "(//input[@maxlength='6']/ancestor::form/preceding::button)[last()]")

    def __init__(
        self,
        driver,
        base_url: str,
        organization: str,
        request_id: str,
        timeout: int = 15,
        slow_motion: float = 0.0,
    ) -> None:
        super().__init__(driver, base_url, timeout, slow_motion)
        self.organization = organization
        self.request_id = request_id

    def open(self) -> None:
        query = urlencode({"organization": self.organization, "requestId": self.request_id})
        self.open_path(f"register?{query}")
        self.wait_until_loaded()

    def open_password(self, email: str, user_id: str) -> None:
        query = urlencode(
            {
                "email": email,
                "userId": user_id,
                "organization": self.organization,
                "requestId": self.request_id,
            }
        )
        self.open_path(f"register/password?{query}")
        self.wait_until_password_loaded()

    def wait_until_loaded(self) -> None:
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(self.title))
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(self.email_input))

    def enter_email(self, email: str) -> None:
        self.type_text(self.email_input, email)

    def continue_to_password(self, email: str) -> None:
        self.enter_email(email)
        self.accept_legal_terms()
        self.click(self.submit_button)
        self.wait_until_password_loaded()

    def accept_legal_terms(self) -> None:
        if not self.is_legal_accepted():
            self.click(self.legal_checkbox)

    def is_legal_accepted(self) -> bool:
        return self.driver.find_element(*self.legal_checkbox).get_attribute("aria-checked") == "true"

    def is_submit_enabled(self) -> bool:
        return self.driver.find_element(*self.submit_button).is_enabled()

    def wait_until_password_loaded(self) -> None:
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(self.password_input))

    def is_password_ui_displayed(self) -> bool:
        required_elements = [self.back_button, self.password_title, self.password_input, self.password_toggle_button]
        return all(self.driver.find_element(*locator).is_displayed() for locator in required_elements)

    def is_password_step_displayed(self) -> bool:
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(self.password_input))
            return True
        except TimeoutException:
            return False

    def enter_password(self, password: str) -> None:
        self.type_text(self.password_input, password)

    def get_password_input_type(self) -> str:
        return self.driver.find_element(*self.password_input).get_attribute("type")

    def toggle_password_visibility(self) -> None:
        self.click(self.password_toggle_button)

    def is_password_rule_matched(self, rule: str) -> bool:
        rule_icon = self.driver.find_element(*self.password_rule_locators[rule])
        return rule_icon.get_attribute("aria-label") in {"Kh\u1edbp", "Matches"}

    def are_all_password_rules_matched(self) -> bool:
        return all(self.is_password_rule_matched(rule) for rule in self.password_rule_locators)

    def click_password_next(self) -> None:
        self.click(self.submit_button)
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(self.referral_input))

    def is_referral_step_displayed(self) -> bool:
        try:
            WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(self.referral_input))
            return True
        except TimeoutException:
            return False

    def is_referral_ui_displayed(self) -> bool:
        required_elements = [
            self.referral_title,
            self.referral_input,
            self.referral_skip_button,
            self.referral_continue_button,
        ]
        return all(self.driver.find_element(*locator).is_displayed() for locator in required_elements)

    def is_referral_continue_enabled(self) -> bool:
        return self.driver.find_element(*self.referral_continue_button).is_enabled()

    def skip_referral(self) -> None:
        self.click(self.referral_skip_button)
        self.wait_until_email_verification_loaded()

    def wait_until_email_verification_loaded(self) -> None:
        WebDriverWait(self.driver, self.timeout).until(
            lambda driver: "/verify" in driver.current_url.lower()
            and len(driver.find_elements(*self.otp_input)) >= 1
        )

    def is_email_verification_displayed(self) -> bool:
        try:
            self.wait_until_email_verification_loaded()
            return True
        except TimeoutException:
            return False

    def is_email_verification_ui_displayed(self) -> bool:
        required_elements = [
            self.email_verify_back_button,
            self.otp_input,
            self.resend_button,
            self.email_verify_next_button,
        ]
        return all(self.driver.find_element(*locator).is_displayed() for locator in required_elements)

    def enter_otp(self, otp: str) -> None:
        self.type_text(self.otp_input, otp)

    def press_otp_backspace(self) -> None:
        self.driver.find_element(*self.otp_input).send_keys(Keys.BACKSPACE)
        self.pause()

    def get_otp_value(self) -> str:
        return self.driver.find_element(*self.otp_input).get_attribute("value")

    def is_email_verify_next_enabled(self) -> bool:
        return self.driver.find_element(*self.email_verify_next_button).is_enabled()

    def is_resend_enabled(self) -> bool:
        return self.driver.find_element(*self.resend_button).is_enabled()

    def click_email_verify_back(self) -> None:
        self.click(self.email_verify_back_button)
        self._confirm_back_if_needed()

    def click_password_back(self) -> None:
        self.click(self.back_button)
        self._confirm_back_if_needed()
        self.wait_until_loaded()

    def _confirm_back_if_needed(self) -> None:
        try:
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(self.confirm_back_button)).click()
            self.pause()
        except TimeoutException:
            return

    def is_email_valid(self) -> bool:
        email = self.driver.find_element(*self.email_input)
        return bool(self.driver.execute_script("return arguments[0].checkValidity();", email))

    def get_email_value(self) -> str:
        return self.driver.find_element(*self.email_input).get_attribute("value")

    def get_link_href(self, locator: tuple[str, str]) -> str:
        return self.driver.find_element(*locator).get_attribute("href")

    def is_initial_ui_displayed(self) -> bool:
        required_elements = [self.title, self.email_input, self.legal_checkbox, self.submit_button, self.login_link]
        return all(self.driver.find_element(*locator).is_displayed() for locator in required_elements)

    def click_login_link(self, index: int = -1) -> None:
        links = self.driver.find_elements(*self.login_link)
        links[index].click()
        WebDriverWait(self.driver, self.timeout).until(EC.url_contains("/loginname"))

    def open_terms_link(self) -> str:
        return self._click_external_link_and_get_url(self.terms_link)

    def open_privacy_link(self) -> str:
        return self._click_external_link_and_get_url(self.privacy_link)

    def open_language_menu(self) -> bool:
        self.click(self.language_button)
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='listbox'], [role='option']"))
            )
            return True
        except TimeoutException:
            return False

    def toggle_dark_mode(self) -> bool:
        was_dark = self._is_dark_mode()
        self.click(self.dark_mode_button)
        WebDriverWait(self.driver, self.timeout).until(lambda _: self._is_dark_mode() != was_dark)
        return self._is_dark_mode() != was_dark

    def _is_dark_mode(self) -> bool:
        html_class = self.driver.find_element(By.TAG_NAME, "html").get_attribute("class") or ""
        return "dark" in html_class.split()

    def _click_external_link_and_get_url(self, locator: tuple[str, str]) -> str:
        original_window = self.driver.current_window_handle
        original_handles = set(self.driver.window_handles)
        self.click(locator)
        WebDriverWait(self.driver, self.timeout).until(lambda driver: len(driver.window_handles) > len(original_handles))
        new_window = next(handle for handle in self.driver.window_handles if handle not in original_handles)
        self.driver.switch_to.window(new_window)
        WebDriverWait(self.driver, self.timeout).until(lambda driver: driver.current_url.startswith("http"))
        current_url = self.driver.current_url
        self.driver.close()
        self.driver.switch_to.window(original_window)
        return current_url
