from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
import os


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _as_int(value: str | None, default: int) -> int:
    if value is None or value.strip() == "":
        return default
    return int(value)


def _as_float(value: str | None, default: float) -> float:
    if value is None or value.strip() == "":
        return default
    return float(value)


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://example.com")
    auth_organization: str = os.getenv("AUTH_ORGANIZATION", "341557029820694806")
    auth_request_id: str = os.getenv("AUTH_REQUEST_ID", "oidc_V2_373571812329521422")
    auth_register_user_id: str = os.getenv("AUTH_REGISTER_USER_ID", "311988438623211354")
    register_test_email: str = os.getenv("REGISTER_TEST_EMAIL", "hainam11993@gmail.com")
    browser: str = os.getenv("BROWSER", "chrome")
    headless: bool = _as_bool(os.getenv("HEADLESS"), False)
    implicit_wait: int = _as_int(os.getenv("IMPLICIT_WAIT"), 0)
    explicit_wait: int = _as_int(os.getenv("EXPLICIT_WAIT"), 15)
    page_load_timeout: int = _as_int(os.getenv("PAGE_LOAD_TIMEOUT"), 30)
    slow_motion: float = _as_float(os.getenv("SLOW_MOTION_SECONDS"), 0.0)
    screenshot_dir: Path = ROOT_DIR / os.getenv("SCREENSHOT_DIR", "reports/screenshots")


def get_settings() -> Settings:
    return Settings()
