from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
import allure
from allure_commons.types import AttachmentType


class BasePage(object):
    __base_url = "https://jira.hillel.it"

    __CORNER_POPUP_MESSAGE = (By.CSS_SELECTOR, ".aui-message")
    __CORNER_POPUP_MESSAGE_ARIA = (By.CSS_SELECTOR, ".aui-flag")

    @allure.step("Init 'BasePage' object")
    def __init__(self, driver):
        self.__driver = driver
        self.__driver.implicitly_wait(10)
        self.__wait = WebDriverWait(self.__driver, 10)

    @property
    def driver(self):
        return self.__driver

    @property
    def wait(self):
        return self.__wait

    @property
    def base_url(self):
        return self.__base_url

    def take_screen(self):
        allure.attach(self.__driver.get_screenshot_as_png(),
                      name="screen.png",
                      attachment_type=AttachmentType.PNG)

    @allure.step
    def wait_element_visible(self, strategy, locator, wait_time=None):
        if wait_time is None:
            wait = self.__wait
        else:
            wait = WebDriverWait(self.__driver, wait_time)

        try:
            element = wait.until(EC.visibility_of_element_located((strategy, locator)))
            return element
        except (TimeoutException, NoSuchElementException):
            self.take_screen()
            raise

    @allure.step
    def wait_element_clickable(self, strategy, locator, wait_time=None):
        if wait_time is None:
            wait = self.__wait
        else:
            wait = WebDriverWait(self.__driver, wait_time)

        try:
            is_clickable = wait.until(EC.element_to_be_clickable((strategy, locator)))
            return is_clickable
        except (TimeoutException, NoSuchElementException):
            self.take_screen()
            raise

    @allure.step
    def wait_element_presence(self, strategy, locator, wait_time=None):
        if wait_time is None:
            wait = self.__wait
        else:
            wait = WebDriverWait(self.__driver, wait_time)

        try:
            is_present = wait.until(EC.presence_of_element_located((strategy, locator)))
            return is_present
        except (TimeoutException, NoSuchElementException):
            self.take_screen()
            raise

    @allure.step
    def find_element(self, strategy, locator, wait_time=None):
        if wait_time is None:
            try:
                element = self.__driver.find_element(strategy, locator)
                return element
            except (TimeoutException, NoSuchElementException):
                self.take_screen()
                raise
        else:
            element = self.wait_element_visible(strategy, locator, wait_time)
            return element

    @allure.step
    def click_element(self, strategy, locator, wait_time=None):
        self.wait_element_clickable(strategy, locator, wait_time)
        self.find_element(strategy, locator).click()

    @allure.step
    def set_element_text(self, text, strategy, locator, wait_time=None):
        self.wait_element_visible(strategy, locator, wait_time)
        self.click_element(strategy, locator, wait_time)
        element = self.find_element(strategy, locator, wait_time)
        element.clear()
        element.send_keys(text)

    @allure.step
    def get_element_text(self, strategy, locator, wait_time=None):
        return self.find_element(strategy, locator, wait_time).text

    @allure.step
    def is_page_opened_by_title(self, title):
        wait = WebDriverWait(self.__driver, 20)
        wait.until(EC.title_contains(title))
        return title in self.__driver.title

    @allure.step
    def is_page_opened_by_url(self, url):
        wait = WebDriverWait(self.__driver, 20)
        wait.until(EC.url_contains(url))
        return url in self.__driver.current_url

    @allure.step
    def find_elements(self, strategy, locator):
        elements = self.__driver.find_elements(strategy, locator)

        if len(elements) == 0:
            self.take_screen()
            raise NoSuchElementException

        return elements

    @allure.step
    def wait_until_text_appeared_in_element(self, text, strategy, locator, wait_time=None):
        if wait_time is None:
            wait = self.__wait
        else:
            wait = WebDriverWait(self.__driver, wait_time)

        try:
            return wait.until(EC.text_to_be_present_in_element((strategy, locator), text))
        except (TimeoutException, NoSuchElementException):
            self.take_screen()
            raise

    @allure.step
    def wait_until_corner_popup_message_is_hidden(self):
        self.wait_element_visible(*self.__CORNER_POPUP_MESSAGE)
        self.wait_until_attribute_equals_str("aria-hidden", "true", *self.__CORNER_POPUP_MESSAGE_ARIA)

    @allure.step
    def wait_until_attribute_equals_str(self, attribute, attribute_value, strategy, locator, wait_time=None):
        if wait_time is None:
            wait_time = 10
        for i in range(1, wait_time):
            element = self.find_element(strategy, locator)
            if element.get_attribute(attribute).lower().strip() == str(attribute_value).lower():
                return True
            time.sleep(1)
        self.take_screen()
        return False
