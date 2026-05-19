from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path

import pytest

from utils.config import get_settings
from utils.driver_factory import create_driver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None, help="Browser: chrome, edge, firefox")
    parser.addoption("--headless", action="store", default=None, help="Run browser in headless mode: true/false")
    parser.addoption("--base-url", action="store", default=None, help="Application base URL")
    parser.addoption("--slow-motion", action="store", default=None, help="Pause seconds after Selenium actions")


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="session")
def base_url(pytestconfig, settings) -> str:
    return pytestconfig.getoption("--base-url") or settings.base_url


@pytest.fixture(scope="session")
def slow_motion(pytestconfig, settings) -> float:
    option = pytestconfig.getoption("--slow-motion")
    return settings.slow_motion if option is None else float(option)


@pytest.fixture
def driver(pytestconfig, settings):
    browser = pytestconfig.getoption("--browser") or settings.browser
    headless_option = pytestconfig.getoption("--headless")
    headless = settings.headless if headless_option is None else headless_option.lower() == "true"

    web_driver = create_driver(browser=browser, headless=headless)
    web_driver.implicitly_wait(settings.implicit_wait)
    web_driver.set_page_load_timeout(settings.page_load_timeout)
    yield web_driver
    web_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    web_driver = item.funcargs.get("driver")
    settings = item.funcargs.get("settings")
    if web_driver is None or settings is None:
        return

    screenshot_dir: Path = settings.screenshot_dir
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = screenshot_dir / f"{item.name}_{timestamp}.png"
    web_driver.save_screenshot(str(screenshot_path))

    extras = getattr(report, "extras", [])
    try:
        import pytest_html

        extras.append(pytest_html.extras.image(os.path.relpath(screenshot_path, Path.cwd())))
        report.extras = extras
    except Exception:
        pass
