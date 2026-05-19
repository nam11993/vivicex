import pytest


@pytest.mark.smoke
def test_browser_can_open_base_url(base_url, request):
    if "your-cex-test-url" in base_url or base_url == "https://example.com":
        pytest.skip("Set BASE_URL in .env or pass --base-url to run browser smoke test.")

    driver = request.getfixturevalue("driver")
    driver.get(base_url)
    assert driver.current_url.startswith("http")
