from pages.base_page import BasePage
from pages.create_issue_page import CreateIssuePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
import allure


class MainPage(BasePage):
    __CREATE_ISSUE_BUTTON = (By.ID, "create_link")
    __ISSUES_MAIN_MENU = (By.ID, "find_link")
    __SEARCH_FOR_ISSUES_MAIN_MENU_ITEM = (By.ID, "issues_new_search_link_lnk")
    __FOCUSED_ISSUE_ITEM = (By.CSS_SELECTOR, "li.focused")
    __CONTAINS_TEXT_SEARCHER_INPUT = (By.ID, "searcher-query")
    __SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-button")
    __NO_ISSUES_FOUND_MESSAGE = (By.CSS_SELECTOR, ".no-results-message")
    __EDIT_ISSUE_SUBMIT_CHANGES_BUTTON = (By.CSS_SELECTOR, ".submit")
    __EDIT_ISSUE_SUMMARY = (By.ID, "summary-val")
    __EDIT_ISSUE_SUMMARY_INPUT = (By.ID, "summary")
    __EDIT_ISSUE_PRIORITY = (By.ID, "priority-val")
    __EDIT_ISSUE_PRIORITY_INPUT = (By.ID, "priority-field")
    __EDIT_ISSUE_ASSIGNEE = (By.ID, "assignee-val")
    __EDIT_ISSUE_ASSIGNEE_INPUT = (By.ID, "assignee-field")

    @allure.step("Init 'MainPage' object")
    def __init__(self, driver):
        super(MainPage, self).__init__(driver)
        self.__logged_in_url = self.base_url + "/projects/WEBINAR/issues"

    @allure.step
    def is_logged_in(self):
        return self.is_page_opened_by_url(self.__logged_in_url)

    @allure.step
    def open_create_issue(self):
        self.wait_element_visible(*self.__FOCUSED_ISSUE_ITEM)
        self.wait_element_clickable(*self.__FOCUSED_ISSUE_ITEM)
        self.wait_element_visible(*self.__CREATE_ISSUE_BUTTON)
        self.click_element(*self.__CREATE_ISSUE_BUTTON)
        self.take_screen()
        return CreateIssuePage(self.driver)

    @allure.step
    def find_issue(self, summary):
        self.search_for_it(summary)

        self.wait_element_visible(*self.__FOCUSED_ISSUE_ITEM)
        self.wait_element_clickable(*self.__FOCUSED_ISSUE_ITEM)

        try:
            is_found = self.wait_until_text_appeared_in_element(summary, *self.__EDIT_ISSUE_SUMMARY)
            self.take_screen()
            return is_found
        except (TimeoutException, NoSuchElementException):
            self.take_screen()
            return False

    @allure.step
    def find_issue_no_results(self, summary):
        self.search_for_it(summary)

        try:
            self.wait_element_visible(*self.__NO_ISSUES_FOUND_MESSAGE)
            self.find_element(*self.__NO_ISSUES_FOUND_MESSAGE)
            self.take_screen()
            return True
        except (TimeoutException, NoSuchElementException):
            self.take_screen()
            return False

    @allure.step
    def search_for_it(self, summary):
        self.wait_element_visible(*self.__ISSUES_MAIN_MENU)
        self.click_element(*self.__ISSUES_MAIN_MENU)
        self.wait_element_visible(*self.__SEARCH_FOR_ISSUES_MAIN_MENU_ITEM)
        self.click_element(*self.__SEARCH_FOR_ISSUES_MAIN_MENU_ITEM)

        self.wait_element_visible(*self.__FOCUSED_ISSUE_ITEM)
        self.wait_element_clickable(*self.__FOCUSED_ISSUE_ITEM)

        self.wait_element_visible(*self.__CONTAINS_TEXT_SEARCHER_INPUT)
        self.click_element(*self.__CONTAINS_TEXT_SEARCHER_INPUT)
        self.set_element_text(summary, *self.__CONTAINS_TEXT_SEARCHER_INPUT)
        self.click_element(*self.__SEARCH_BUTTON)

    @allure.step
    def update_issue_summary(self, summary):
        self.click_element(*self.__EDIT_ISSUE_SUMMARY)
        self.set_element_text(summary + Keys.ENTER, *self.__EDIT_ISSUE_SUMMARY_INPUT)
        is_updated = self.wait_until_text_appeared_in_element(summary, *self.__EDIT_ISSUE_SUMMARY)
        self.take_screen()
        return is_updated

    @allure.step
    def update_issue_priority(self, priority):
        self.click_element(*self.__EDIT_ISSUE_PRIORITY)
        self.set_element_text(priority + Keys.ENTER, *self.__EDIT_ISSUE_PRIORITY_INPUT)
        self.click_element(*self.__EDIT_ISSUE_SUBMIT_CHANGES_BUTTON)
        self.find_element(*self.__EDIT_ISSUE_PRIORITY)
        is_updated = self.wait_until_text_appeared_in_element(priority, *self.__EDIT_ISSUE_PRIORITY)
        self.take_screen()
        return is_updated

    @allure.step
    def update_issue_assignee(self, assignee):
        self.click_element(*self.__EDIT_ISSUE_ASSIGNEE)
        self.set_assignee_text(assignee + Keys.ENTER, *self.__EDIT_ISSUE_ASSIGNEE_INPUT)
        self.click_element(*self.__EDIT_ISSUE_SUBMIT_CHANGES_BUTTON)
        self.find_element(*self.__EDIT_ISSUE_ASSIGNEE)
        is_updated = self.wait_until_text_appeared_in_element(assignee, *self.__EDIT_ISSUE_ASSIGNEE)
        self.take_screen()
        return is_updated

    @allure.step
    def set_assignee_text(self, text, strategy, locator, wait_time=None):
        self.wait_element_visible(strategy, locator, wait_time)
        self.click_element(strategy, locator, wait_time)
        element = self.find_element(strategy, locator, wait_time)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(text)
