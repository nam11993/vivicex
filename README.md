# CEX Automation Test Framework

Stack: Python, Selenium WebDriver, Pytest, pytest-html, Page Object Model, Excel test data.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Update `.env` with the real CEX test URL and account.

## Run tests

```powershell
pytest
pytest -m smoke
pytest -m register
pytest -m login --base-url=https://your-test-env.example
pytest --browser=chrome --headless=true
```

The HTML report is written to `reports/report.html`. Failed test screenshots are written to `reports/screenshots`.

## Test data

Login data lives in `test_data/users.xlsx`, sheet `login`.

Columns:

```text
case_id, email, password, expected_result, note
```

Use `success` or `failed` in `expected_result`.

## Register UI tests

Register cases are read from `test_data/users.xlsx`, sheet `login`, for the UI-safe `REG_*` cases marked `Auto=Yes`.

```powershell
pytest -m register
```
