import re
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect, Page


from tests.pages.login_page import CustomerLoginPage

@pytest.mark.functional
@pytest.mark.login
def test_login_with_valid_account(page: Page):
    """success login"""
    login_page = CustomerLoginPage(page)
    login_page.open()

    login_page.login("emma.scott.3012","Emma")
    login_page.validate_ticket_page_is_open()

@pytest.mark.functional
@pytest.mark.login
@pytest.mark.login_negative
def test_login_invalid_credential(page: Page):
    """success login"""
    login_page = CustomerLoginPage(page)
    login_page.open()

    login_page.login("emma.scott.3012","Emmas")
    login_page.validate_error_message_invalid_creds_is_shown()
