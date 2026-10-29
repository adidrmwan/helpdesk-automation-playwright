from playwright.sync_api import Page
import allure

class BasePage:

    path = "/"

    def __init__(self, page:Page):
        self.page = page

    @allure.step("open browser")
    def open(self):
        self.page.goto(self.path)