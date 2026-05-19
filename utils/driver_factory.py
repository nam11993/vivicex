from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def create_driver(browser: str = "chrome", headless: bool = False) -> webdriver.Remote:
    browser_name = browser.strip().lower()

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    if browser_name == "edge":
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        return webdriver.Edge(options=options)

    if browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    raise ValueError(f"Unsupported browser: {browser}")
