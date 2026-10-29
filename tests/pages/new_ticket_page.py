from .base_page import BasePage
from playwright.sync_api import Page,expect
import allure

class NewTicketPage(BasePage):
    path = "/customer/tickets/new"

    def __init__(self, page):
        super().__init__(page)
        self.new_ticket_title = page.get_by_text("Create New Support Ticket")
        self.subject_input = page.get_by_role("textbox", name="Subject *")
        self.priority_input = page.get_by_label("Priority")
        self.description_input = page.get_by_role("textbox", name="Description *").get_by_role("textbox")
        self.cancel_btn = page.get_by_role("button", name="Cancel")
        self.create_ticket_btn = page.get_by_role("button", name="Create Ticket")
        self.close_ticket_btn = page.get_by_role("button", name="Close Ticket")
        self.got_it_btn = page.get_by_role("button", name="Got it!")
        self.new_icon = page.get_by_text("new")
        self.subject_value = page.locator(".gk-text-gradient")
        self.message_value = page.locator("[data-article-body]")

    @allure.step("validate ticket page is open")
    def new_ticket_page_is_open(self):
        expect(self.new_ticket_title).to_be_visible()

    @allure.step("select priority")
    def choose_priority(self, label):
        self.priority_input.select_option(label=label)

    @allure.step("create ticket with {subject} and {message}")
    def create_ticket(self, subject, message,priority=None):
        self.got_it_btn.click()
        self.subject_input.fill(subject)
        if priority:
            self.choose_priority(priority)
        self
        self.description_input.fill(message)
        self.create_ticket_btn.click()
        expect(self.close_ticket_btn).to_be_visible()

    @allure.step("new ticket is created")
    def validate_new_ticket_is_created(self,subject,message):
        expect(self.subject_value).to_have_text(subject)
        expect(self.message_value).to_have_text(message)

    @allure.step("click close button")
    def click_closed_btn(self):
        self.close_ticket_btn.click()