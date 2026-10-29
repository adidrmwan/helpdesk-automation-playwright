import re,pytest
from playwright.sync_api import expect

from tests.pages.my_tickets_page import MyTicketsPage
from tests.pages.new_ticket_page import NewTicketPage

@pytest.mark.e2e
def test_create_new_ticket(customer_page):
    new_ticket = NewTicketPage(customer_page)
    my_tickets = MyTicketsPage(customer_page)

    my_tickets.open()
    my_tickets.click_create_new_ticket()
    new_ticket.new_ticket_page_is_open()
    new_ticket.create_ticket("tiket baru testing", "testing sahaja")
    new_ticket.validate_new_ticket_is_created("tiket baru testing","testing sahaja")
    new_ticket.click_closed_btn()
