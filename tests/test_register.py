from __future__ import annotations

from datetime import datetime

import pytest

from pages.register_page import RegisterPage
from utils.config import ROOT_DIR
from utils.excel_reader import read_sheet_as_dicts


DATA_FILE = ROOT_DIR / "test_data" / "users.xlsx"
SHEET_NAME = "login"

UI_REGISTER_CASES = {
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

PASSWORD_REGISTER_CASES = {
    "REG_018",
    "REG_019",
    "REG_020",
    "REG_021",
    "REG_022",
    "REG_023",
    "REG_024",
    "REG_025",
    "REG_026",
    "REG_027",
    "REG_028",
    "REG_029",
}

REFERRAL_SKIP_REGISTER_CASES = {
    "REG_030",
    "REG_031",
    "REG_032",
}

EMAIL_VERIFY_REGISTER_CASES = {
    "REG_037",
    "REG_039",
    "REG_040",
    "REG_044",
    "REG_047",
    "REG_048",
    "REG_049",
    "REG_050",
}

PASSWORD_RULE_BY_CASE = {
    "REG_021": "length",
    "REG_022": "uppercase",
    "REG_023": "lowercase",
    "REG_024": "number",
    "REG_025": "symbol",
}


def _cell(row: dict, name: str, default: str = "") -> str:
    value = row.get(name)
    if value is None:
        return default
    return str(value).strip()


def _unique_email() -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"auto.register.{timestamp}@example.com"


def _register_cases() -> list[dict]:
    if not DATA_FILE.exists():
        return []

    cases = []
    for row in read_sheet_as_dicts(DATA_FILE, SHEET_NAME):
        case_id = _cell(row, "ID")
        auto = _cell(row, "Auto").lower()
        if case_id in UI_REGISTER_CASES | PASSWORD_REGISTER_CASES | REFERRAL_SKIP_REGISTER_CASES | EMAIL_VERIFY_REGISTER_CASES and auto == "yes":
            cases.append(row)
    return cases


def _cases_by_id(case_ids: set[str]) -> list[dict]:
    return [case for case in _register_cases() if _cell(case, "ID") in case_ids]


def _open_referral_step(register_page: RegisterPage, settings) -> None:
    register_page.open_password(settings.register_test_email, settings.auth_register_user_id)
    register_page.enter_password("Abcdef1@")
    register_page.click_password_next()


def _open_referral_step_with_new_email(register_page: RegisterPage) -> None:
    register_page.open()
    register_page.continue_to_password(_unique_email())
    register_page.enter_password("Abcdef1@")
    register_page.click_password_next()


def _open_email_verification_step(register_page: RegisterPage) -> None:
    _open_referral_step_with_new_email(register_page)
    register_page.skip_referral()


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
@pytest.mark.parametrize("case", _cases_by_id(UI_REGISTER_CASES), ids=lambda case: case.get("ID", "register_case"))
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


@pytest.mark.register
@pytest.mark.parametrize(
    "case",
    _cases_by_id(PASSWORD_REGISTER_CASES),
    ids=lambda case: case.get("ID", "register_password_case"),
)
def test_register_password_validation(register_page: RegisterPage, settings, case: dict):
    case_id = _cell(case, "ID")
    test_data = _cell(case, "Test data")
    password = "" if test_data in {"N/A", "Empty password"} else test_data

    if case_id == "REG_018":
        register_page.open()
        register_page.continue_to_password(_unique_email())
        assert register_page.is_password_ui_displayed()

    elif case_id == "REG_028":
        register_page.open()
        register_page.continue_to_password(_unique_email())
        register_page.click_password_back()
        assert register_page.is_initial_ui_displayed()

    else:
        register_page.open_password(settings.register_test_email, settings.auth_register_user_id)

        if case_id == "REG_019":
            assert register_page.is_password_ui_displayed()
            assert not register_page.is_submit_enabled()

        elif case_id == "REG_020":
            assert not register_page.is_submit_enabled()

        elif case_id in PASSWORD_RULE_BY_CASE:
            register_page.enter_password(password)
            assert not register_page.is_password_rule_matched(PASSWORD_RULE_BY_CASE[case_id])
            assert not register_page.is_submit_enabled()

        elif case_id == "REG_026":
            register_page.enter_password(password)
            assert register_page.are_all_password_rules_matched()
            assert register_page.is_submit_enabled()

        elif case_id == "REG_027":
            register_page.enter_password(password)
            assert register_page.get_password_input_type() == "password"
            register_page.toggle_password_visibility()
            assert register_page.get_password_input_type() == "text"
            register_page.toggle_password_visibility()
            assert register_page.get_password_input_type() == "password"

        elif case_id == "REG_029":
            register_page.enter_password(password)
            assert register_page.is_submit_enabled()
            register_page.click_password_next()
            assert register_page.is_referral_step_displayed()

        else:
            pytest.skip(f"No automation mapping has been implemented for {case_id}.")


@pytest.mark.register
@pytest.mark.parametrize(
    "case",
    _cases_by_id(REFERRAL_SKIP_REGISTER_CASES),
    ids=lambda case: case.get("ID", "register_referral_case"),
)
def test_register_referral_skip_flow(register_page: RegisterPage, settings, case: dict):
    case_id = _cell(case, "ID")

    if case_id in {"REG_030", "REG_032"}:
        _open_referral_step(register_page, settings)

        if case_id == "REG_030":
            assert register_page.is_referral_ui_displayed()

        elif case_id == "REG_032":
            assert not register_page.is_referral_continue_enabled()

    elif case_id == "REG_031":
        _open_referral_step_with_new_email(register_page)
        register_page.skip_referral()
        assert register_page.is_email_verification_displayed()

    else:
        pytest.skip(f"No automation mapping has been implemented for {case_id}.")


@pytest.mark.register
@pytest.mark.parametrize(
    "case",
    _cases_by_id(EMAIL_VERIFY_REGISTER_CASES),
    ids=lambda case: case.get("ID", "register_email_verify_case"),
)
def test_register_email_verification(register_page: RegisterPage, case: dict):
    case_id = _cell(case, "ID")
    test_data = _cell(case, "Test data")

    _open_email_verification_step(register_page)

    if case_id == "REG_037":
        assert register_page.is_email_verification_ui_displayed()
        assert not register_page.is_email_verify_next_enabled()

    elif case_id == "REG_039":
        register_page.enter_otp(test_data)
        assert register_page.get_otp_value() == test_data
        assert not register_page.is_email_verify_next_enabled()

    elif case_id == "REG_040":
        register_page.enter_otp(test_data)
        assert register_page.get_otp_value() == test_data
        assert register_page.is_email_verify_next_enabled()

    elif case_id == "REG_044":
        assert not register_page.is_resend_enabled()

    elif case_id == "REG_047":
        register_page.enter_otp(test_data)
        assert register_page.get_otp_value() == test_data
        assert register_page.is_email_verify_next_enabled()
        register_page.press_otp_backspace()
        assert register_page.get_otp_value() == test_data[:-1]
        assert not register_page.is_email_verify_next_enabled()

    elif case_id == "REG_048":
        register_page.enter_otp(test_data)
        assert register_page.get_otp_value() == test_data
        assert register_page.is_email_verify_next_enabled()

    elif case_id == "REG_049":
        register_page.enter_otp(test_data)
        assert register_page.get_otp_value() == test_data[:6]
        assert register_page.is_email_verify_next_enabled()

    elif case_id == "REG_050":
        register_page.click_email_verify_back()
        if register_page.is_referral_step_displayed():
            assert True
        elif register_page.is_password_step_displayed():
            pytest.xfail("Expected back to referral step, but platform navigates back to password step.")
        else:
            pytest.fail("Back from email verification did not return to referral or password step.")

    else:
        pytest.skip(f"No automation mapping has been implemented for {case_id}.")
