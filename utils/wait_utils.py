from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_visible(driver: WebDriver, locator: tuple[str, str], timeout: int = 15):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def wait_for_clickable(driver: WebDriver, locator: tuple[str, str], timeout: int = 15):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def wait_for_url_contains(driver: WebDriver, text: str, timeout: int = 15) -> bool:
    return WebDriverWait(driver, timeout).until(EC.url_contains(text))
