import re

import pytest,allure
from playwright.sync_api import expect
from pathlib import Path
from tests import config

from tests.pages.login_page import CustomerLoginPage

@pytest.fixture(scope="session")
def base_url():
    """Alamat aplikasi. Karena ini, test cukup menulis page.goto("/login")."""
    return config.BASE_URL


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Pengaturan browser: ukuran jendela dan bahasa."""
    settings = dict(browser_context_args)
    settings["viewport"] = {"width": 1280, "height": 800}
    settings["locale"] = "en-US"
    return settings

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    settings = dict(browser_type_launch_args)
    settings["headless"] = False
    settings["slow_mo"] = 500
    return settings


@pytest.fixture
def page(page):
    """Tab browser baru untuk setiap test + timeout 15 detik."""
    page.set_default_timeout(config.DEFAULT_TIMEOUT_MS)
    return page


@pytest.fixture
def customer_login_page(page):
    return CustomerLoginPage(page)

@pytest.fixture
def customer_page(page):
    login_page = CustomerLoginPage(page)
    login_page.open()
    login_page.login(config.CUSTOMER_LOGIN,config.CUSTOMER_PASSWORD)
    login_page.validate_ticket_page_is_open()

    return page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item,call):
    outcome = yield
    report = outcome.get_result()
    page = item.funcargs.get("page")

    if report.when == "call" and report.failed and page is not None:
        allure.attach(page.screenshot(full_page=True), name="screenshot", attachment_type=allure.attachment_type.PNG)
        allure.attach(page.url, name="alamat halaman", attachment_type=allure.attachment_type.TEXT)
        item.test_failed = True

    if report.when == "teardown" and getattr(item, "test_failed", False):
        trace_file = Path(item.funcargs["output_path"]) / "trace.zip"
        if trace_file.exists():
            allure.attach.file(str(trace_file), name="trace.zip (open with playwright show-trace)", attachment_type=allure.attachment_type.ZIP)