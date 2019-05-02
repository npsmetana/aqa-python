from pages.base_page import BasePage
from pages.create_issue_page import CreateIssuePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class MainPage(BasePage):
    __CREATE_ISSUE_BUTTON = (By.ID, "create_link")
    __VIEW_ALL_FILTERS_LINK = (By.CSS_SELECTOR, "#full-issue-navigator>a")
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
    __EDIT_ISSUE_ASSIGNEE_TEXT_CONTAINER = (By.CSS_SELECTOR, "#assignee-val>.user-hover")
    __ISSUE_MORE_ACTIONS_DROPDOWN = (By.ID, "opsbar-operations_more")
    __ISSUE_ACTION_DELETE_ITEM = (By.CSS_SELECTOR, "aui-item-link.issueaction-delete-issue")
    __CONFIRM_DELETE_BUTTON = (By.ID, "delete-issue-submit")
    __ORDER_BY_BUTTON = (By.CSS_SELECTOR, ".order-by")

    def __init__(self, driver):
        super(MainPage, self).__init__(driver)
        self.__logged_in_url = self.base_url + "/projects/WEBINAR/issues"
        self.__logout_url = self.base_url + "/secure/Logout.jsp"

    def is_logged_in(self):
        return self.is_page_opened_by_url(self.__logged_in_url)

    def open_create_issue(self):
        self.wait_element_visible(*self.__ORDER_BY_BUTTON)
        self.wait_element_clickable(*self.__ORDER_BY_BUTTON)
        self.wait_element_visible(*self.__CREATE_ISSUE_BUTTON)
        self.click_element(*self.__CREATE_ISSUE_BUTTON)
        return CreateIssuePage(self.driver)

    def enable_all_search_filters(self):
        self.wait_until_corner_popup_message_is_hidden()

        self.wait_element_visible(*self.__VIEW_ALL_FILTERS_LINK)
        self.click_element(*self.__VIEW_ALL_FILTERS_LINK)
        self.wait_element_visible(*self.__ORDER_BY_BUTTON)
        self.find_element(*self.__ORDER_BY_BUTTON)

    def find_issue(self, summary, reset_search):
        issue_found = False

        self.search_for_it(summary)

        try:
            issue_found = self.wait_till_text_appeared_in_element(summary, *self.__EDIT_ISSUE_SUMMARY)
        except (TimeoutException, NoSuchElementException):
            pass

        if reset_search:
            self.search_for_it("")

        return issue_found

    def find_issue_no_results(self, summary, reset_search):
        check_passed = False

        self.search_for_it(summary)

        try:
            self.find_element(*self.__NO_ISSUES_FOUND_MESSAGE)
            check_passed = True
        except (TimeoutException, NoSuchElementException):
            pass

        if reset_search:
            self.search_for_it("")
        return check_passed

    def search_for_it(self, summary):
        self.wait_element_visible(*self.__SEARCH_BUTTON)
        self.wait_element_clickable(*self.__SEARCH_BUTTON)

        self.wait_element_visible(*self.__CONTAINS_TEXT_SEARCHER_INPUT)
        self.click_element(*self.__CONTAINS_TEXT_SEARCHER_INPUT)
        self.set_element_text(summary, *self.__CONTAINS_TEXT_SEARCHER_INPUT)
        self.click_element(*self.__SEARCH_BUTTON)

    def update_issue_summary(self, summary):
        self.click_element(*self.__EDIT_ISSUE_SUMMARY)
        self.set_element_text(summary + Keys.ENTER, *self.__EDIT_ISSUE_SUMMARY_INPUT)
        return self.wait_till_text_appeared_in_element(summary, *self.__EDIT_ISSUE_SUMMARY)

    def update_issue_priority(self, priority):
        self.click_element(*self.__EDIT_ISSUE_PRIORITY)
        self.set_element_text(priority + Keys.ENTER, *self.__EDIT_ISSUE_PRIORITY_INPUT)
        self.click_element(*self.__EDIT_ISSUE_SUBMIT_CHANGES_BUTTON)
        self.find_element(*self.__EDIT_ISSUE_PRIORITY)
        return self.wait_till_text_appeared_in_element(priority, *self.__EDIT_ISSUE_PRIORITY)

    def update_issue_assignee(self, assignee):
        self.click_element(*self.__EDIT_ISSUE_ASSIGNEE)
        self.set_assignee_text(assignee + Keys.ENTER, *self.__EDIT_ISSUE_ASSIGNEE_INPUT)
        self.wait_element_visible(*self.__EDIT_ISSUE_SUBMIT_CHANGES_BUTTON)
        self.click_element(*self.__EDIT_ISSUE_SUBMIT_CHANGES_BUTTON)
        self.find_element(*self.__EDIT_ISSUE_ASSIGNEE)
        return self.wait_till_text_appeared_in_element(assignee, *self.__EDIT_ISSUE_ASSIGNEE)

    def set_assignee_text(self, text, strategy, locator, wait_time=None):
        self.wait_element_visible(strategy, locator, wait_time)
        self.click_element(strategy, locator, wait_time)
        element = self.find_element(strategy, locator, wait_time)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(text)
