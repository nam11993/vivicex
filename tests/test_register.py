from __future__ import annotations

import pytest

from pages.register_page import RegisterPage
from utils.config import ROOT_DIR
from utils.excel_reader import read_sheet_as_dicts


DATA_FILE = ROOT_DIR / "test_data" / "users.xlsx"
SHEET_NAME = "login"

UI_SAFE_REGISTER_CASES = {
    "REG_001",
    "REG_002",
    "REG_003",
    "REG_004",
    "REG_005",
    "REG_006",
    "REG_007",
    "REG_008",
    "REG_009",
    "REG_012",
    "REG_013",
    "REG_014",
    "REG_015",
    "REG_016",
    "REG_017",
}


def _cell(row: dict, name: str, default: str = "") -> str:
    value = row.get(name)
    if value is None:
        return default
    return str(value).strip()


def _register_cases() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    cases = []
    for row in read_sheet_as_dicts(DATA_FILE, SHEET_NAME):
        case_id = _cell(row, "ID")
        auto = _cell(row, "Auto").lower()
        if case_id in UI_SAFE_REGISTER_CASES and auto == "yes":
            cases.append(row)
    return cases


@pytest.fixture
def register_page(driver, base_url, settings, slow_motion) -> RegisterPage:
    return RegisterPage(
        driver=driver,
        base_url=base_url,
        organization=settings.auth_organization,
        request_id=settings.auth_request_id,
        timeout=settings.explicit_wait,
        slow_motion=slow_motion,
    )


@pytest.mark.register
@pytest.mark.parametrize("case", _register_cases(), ids=lambda case: case.get("ID", "register_case"))
def test_register_ui_validation(register_page: RegisterPage, case: dict):
    case_id = _cell(case, "ID")
    test_data = _cell(case, "Test data")

    register_page.open()

    if case_id == "REG_001":
        assert register_page.is_initial_ui_displayed()
        assert not register_page.is_submit_enabled()

    elif case_id == "REG_002":
        assert register_page.get_email_value() == ""
        assert not register_page.is_legal_accepted()
        assert not register_page.is_submit_enabled()

    elif case_id == "REG_003":
        register_page.enter_email(test_data)
        assert register_page.is_email_valid()
        assert not register_page.is_legal_accepted()
        assert not register_page.is_submit_enabled()

    elif case_id == "REG_004":
        register_page.accept_legal_terms()
        assert register_page.get_email_value() == ""
        assert register_page.is_legal_accepted()
        assert not register_page.is_submit_enabled()

    elif case_id == "REG_005":
        register_page.enter_email(test_data)
        register_page.accept_legal_terms()
        assert register_page.is_email_valid()
        assert register_page.is_legal_accepted()
        assert register_page.is_submit_enabled()

    elif case_id == "REG_006":
        register_page.enter_email(test_data)
        assert register_page.is_email_valid()
        assert not register_page.is_legal_accepted()
        assert not register_page.is_submit_enabled()

    elif case_id in {"REG_007", "REG_008", "REG_009"}:
        register_page.enter_email(test_data)
        register_page.accept_legal_terms()
        assert not register_page.is_email_valid()
        assert register_page.is_legal_accepted()

    elif case_id == "REG_012":
        href = register_page.get_link_href(register_page.terms_link)
        assert "terms-and-conditions" in href
        opened_url = register_page.open_terms_link()
        assert "terms-and-conditions" in opened_url

    elif case_id == "REG_013":
        href = register_page.get_link_href(register_page.privacy_link)
        assert "privacy-policy" in href
        opened_url = register_page.open_privacy_link()
        assert "privacy-policy" in opened_url

    elif case_id == "REG_014":
        register_page.click_login_link(index=-1)
        assert "/loginname" in register_page.driver.current_url

    elif case_id == "REG_015":
        register_page.click_login_link(index=0)
        assert "/loginname" in register_page.driver.current_url

    elif case_id == "REG_016":
        assert register_page.open_language_menu()

    elif case_id == "REG_017":
        assert register_page.toggle_dark_mode()

    else:
        pytest.skip(f"No automation mapping has been implemented for {case_id}.")
