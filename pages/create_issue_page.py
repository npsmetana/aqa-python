from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from pynput.keyboard import Key, Controller
import allure


class CreateIssuePage(BasePage):
    __CREATE_ISSUE_BUTTON = (By.ID, "create-issue-submit")
    __CANCEL_ISSUE_BUTTON = (By.CSS_SELECTOR, "#create-issue-dialog .cancel")
    __ISSUE_TYPE_INPUT = (By.ID, "issuetype-field")
    __ISSUE_SUMMARY_INPUT = (By.ID, "summary")
    __SUMMARY_ERROR_MESSAGE = (By.CSS_SELECTOR, ".error[data-field='summary']")

    @allure.step("Init 'CreateIssuePage' object")
    def __init__(self, driver):
        super(CreateIssuePage, self).__init__(driver)

    @allure.step
    def create_issue(self, summary):
        self.click_element(*self.__ISSUE_TYPE_INPUT)
        self.set_element_text("Bug" + Keys.ENTER, *self.__ISSUE_TYPE_INPUT)

        self.click_element(*self.__ISSUE_SUMMARY_INPUT)
        self.set_element_text(summary, *self.__ISSUE_SUMMARY_INPUT)
        self.take_screen()

        self.click_element(*self.__CREATE_ISSUE_BUTTON)
        self.take_screen()

        self.wait_until_corner_popup_message_is_hidden()
        self.take_screen()

    @allure.step
    def cancel_creation(self):
        self.click_element(*self.__CANCEL_ISSUE_BUTTON)

        # "Cancel create issue" popup can't be recognized/controlled via Selenium
        # So just direct 'time.sleep()' waits are used
        keyboard = Controller()
        time.sleep(1)
        keyboard.press(Key.enter)
        time.sleep(0.5)
        keyboard.release(Key.enter)

    @allure.step
    def create_issue_no_summary(self):
        check_passed = False

        self.wait_element_visible(*self.__CREATE_ISSUE_BUTTON)
        self.click_element(*self.__CREATE_ISSUE_BUTTON)

        try:
            text = self.get_element_text(*self.__SUMMARY_ERROR_MESSAGE)
            check_passed = (text.strip() == "You must specify a summary of the issue.")
        except (TimeoutException, NoSuchElementException):
            pass

        self.take_screen()
        self.cancel_creation()
        return check_passed

    @allure.step
    def create_issue_too_long_summary(self):
        check_passed = False

        too_long_summary = "z" * 256
        self.click_element(*self.__ISSUE_SUMMARY_INPUT)
        self.set_element_text(too_long_summary, *self.__ISSUE_SUMMARY_INPUT)
        self.click_element(*self.__CREATE_ISSUE_BUTTON)

        try:
            text = self.get_element_text(*self.__SUMMARY_ERROR_MESSAGE)
            check_passed = (text.strip() == "Summary must be less than 255 characters.")
        except (TimeoutException, NoSuchElementException):
            pass

        self.take_screen()
        self.cancel_creation()
        return check_passed

