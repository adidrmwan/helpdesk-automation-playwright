from .base_page import BasePage
from playwright.sync_api import Page,expect
import allure

class MyTicketsPage(BasePage):
    path = "/customer/tickets"

    def __init__(self, page):
        super().__init__(page)
        self.title_my_ticket = page.get_by_text("My Tickets")
        self.search_input = page.get_by_role("textbox", name="Search by ticket number or")
        self.search_btn = page.get_by_role("button", name="Search")
        self.clear_btn = page.get_by_role("link", name="Clear")
        self.create_new_ticket_btn = page.get_by_role("link", name="Create New Ticket")
        self.got_it_btn = page.get_by_role("button", name="Got it!")

    @allure.step("click create new ticket button")
    def click_create_new_ticket(self):
        expect(self.title_my_ticket).to_be_visible()
        self.got_it_btn.click()
        self.create_new_ticket_btn.click()

    @allure.step("search item")
    def search(self,text):
        self.search_input.fill(text)
        self.search_btn.click()

    


