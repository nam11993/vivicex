from pathlib import Path
import os

import pytest

from pages.login_page import LoginPage
from utils.config import ROOT_DIR
from utils.excel_reader import read_sheet_as_dicts


DATA_FILE = ROOT_DIR / "test_data" / "users.xlsx"


def _login_cases():
    if not DATA_FILE.exists():
        return []
    cases = []
    for row in read_sheet_as_dicts(DATA_FILE, "login"):
        case_id = row.get("case_id") or row.get("ID")
        if case_id and str(case_id).startswith("LOGIN_"):
            cases.append(row)
    return cases


@pytest.mark.login
@pytest.mark.parametrize("case", _login_cases(), ids=lambda case: case.get("case_id") or case.get("ID", "login_case"))
def test_login_from_excel(base_url, settings, case, request):
    if base_url == "https://example.com" or "your-cex-test-url" in base_url:
        pytest.skip("Set BASE_URL in .env or pass --base-url to run login tests.")

    email = case.get("email") or os.getenv("TEST_EMAIL")
    password = case.get("password") or os.getenv("TEST_PASSWORD")
    expected_result = str(case.get("expected_result") or "success").lower()

    if not email or not password:
        pytest.skip("Fill login test data in test_data/users.xlsx or .env first.")

    driver = request.getfixturevalue("driver")
    page = LoginPage(
        driver,
        base_url,
        timeout=settings.explicit_wait,
        email_selector=os.getenv("LOGIN_EMAIL_SELECTOR", "id=email"),
        password_selector=os.getenv("LOGIN_PASSWORD_SELECTOR", "id=password"),
        submit_selector=os.getenv("LOGIN_SUBMIT_SELECTOR", "css=button[type='submit']"),
        error_selector=os.getenv("LOGIN_ERROR_SELECTOR", "css=.error,.alert,[role='alert']"),
        logged_in_selector=os.getenv("LOGGED_IN_SELECTOR", "css=[data-testid='user-menu'],.user-menu,.account-menu"),
    )
    page.open()
    page.login(str(email), str(password))

    if expected_result == "success":
        assert page.is_logged_in(), "Expected successful login, but logged-in marker was not visible."
    else:
        assert page.has_error_message(), "Expected login error message, but none was visible."
