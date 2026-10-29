from playwright.sync_api import Page,expect
import allure

from .base_page import BasePage

class CustomerLoginPage(BasePage):


    path = "/customer/login"

    def __init__(self, page:Page):
        super().__init__(page)

        self.title_customer_login = page.get_by_role("heading", name="Customer Support Login")
        self.username_input = page.get_by_role("textbox", name="Login")
        self.password_input = page.get_by_role("textbox", name="Password")
        self.login_btn = page.get_by_role("button", name="Sign in")
        self.title_tickets_page = page.get_by_text("My Tickets")
        self.error_message_invalid_creds = page.get_by_text("invalid credentials")

    @allure.step("success login {username}")
    def login(self, username: str, password: str):
        expect(self.title_customer_login).to_be_visible()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_btn.click()
    
    @allure.step("validate ticket page is open")
    def validate_ticket_page_is_open(self):
        expect(self.title_tickets_page).to_be_visible()

    @allure.step("error message is shown")
    def validate_error_message_invalid_creds_is_shown(self):
        expect(self.error_message_invalid_creds).to_be_visible
