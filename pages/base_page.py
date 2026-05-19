from __future__ import annotations

from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from utils.wait_utils import wait_for_clickable, wait_for_visible


LOCATOR_MAP = {
    "id": By.ID,
    "name": By.NAME,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "class": By.CLASS_NAME,
    "tag": By.TAG_NAME,
    "link": By.LINK_TEXT,
    "partial_link": By.PARTIAL_LINK_TEXT,
}


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 15, slow_motion: float = 0.0) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.slow_motion = slow_motion

    def build_url(self, path: str = "") -> str:
        if not path:
            return self.base_url
        return f"{self.base_url}/{path.lstrip('/')}"

    def parse_locator(self, locator_value: str) -> tuple[str, str]:
        strategy, value = locator_value.split("=", 1)
        by = LOCATOR_MAP.get(strategy.strip().lower())
        if by is None:
            raise ValueError(f"Unsupported locator strategy: {strategy}")
        return by, value.strip()

    def open_path(self, path: str = "") -> None:
        self.driver.get(self.build_url(path))
        self.pause()

    def type_text(self, locator: tuple[str, str], text: str) -> None:
        element = wait_for_visible(self.driver, locator, self.timeout)
        element.clear()
        element.send_keys(text)
        self.pause()

    def click(self, locator: tuple[str, str]) -> None:
        wait_for_clickable(self.driver, locator, self.timeout).click()
        self.pause()

    def visible_text(self, locator: tuple[str, str]) -> str:
        return wait_for_visible(self.driver, locator, self.timeout).text

    def pause(self) -> None:
        if self.slow_motion > 0:
            sleep(self.slow_motion)
