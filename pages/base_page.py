from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time


class BasePage(object):
    __base_url = "https://jira.hillel.it"

    __CORNER_POPUP_MESSAGE = (By.CSS_SELECTOR, ".aui-message")

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

    def wait_element_visible(self, strategy, locator, wait_time=None):
        if wait_time is None:
            wait = self.__wait
        else:
            wait = WebDriverWait(self.__driver, wait_time)

        try:
            element = wait.until(EC.visibility_of_element_located((strategy, locator)))
            return element
        except (TimeoutException, NoSuchElementException):
            raise

    def wait_element_clickable(self, strategy, locator, wait_time=None):
        if wait_time is None:
            wait = self.__wait
        else:
            wait = WebDriverWait(self.__driver, wait_time)

        try:
            is_clickable = wait.until(EC.element_to_be_clickable((strategy, locator)))
            return is_clickable
        except (TimeoutException, NoSuchElementException):
            raise

    def wait_element_presence(self, strategy, locator, wait_time=None):
        if wait_time is None:
            wait = self.__wait
        else:
            wait = WebDriverWait(self.__driver, wait_time)

        try:
            is_present = wait.until(EC.presence_of_element_located((strategy, locator)))
            return is_present
        except (TimeoutException, NoSuchElementException):
            raise

    def find_element(self, strategy, locator, wait_time=None):
        if wait_time is None:
            try:
                element = self.__driver.find_element(strategy, locator)
                return element
            except (TimeoutException, NoSuchElementException):
                raise
        else:
            element = self.wait_element_visible(strategy, locator, wait_time)
            return element

    def click_element(self, strategy, locator, wait_time=None):
        self.wait_element_clickable(strategy, locator, wait_time)
        self.find_element(strategy, locator).click()

    def set_element_text(self, text, strategy, locator, wait_time=None):
        self.wait_element_visible(strategy, locator, wait_time)
        self.click_element(strategy, locator, wait_time)
        element = self.find_element(strategy, locator, wait_time)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, strategy, locator, wait_time=None):
        return self.find_element(strategy, locator, wait_time).text

    def is_page_opened_by_title(self, title):
        wait = WebDriverWait(self.__driver, 20)
        wait.until(EC.title_contains(title))
        return title in self.__driver.title

    def is_page_opened_by_url(self, url):
        wait = WebDriverWait(self.__driver, 20)
        wait.until(EC.url_contains(url))
        return url in self.__driver.current_url

    def find_elements(self, strategy, locator):
        elements = self.__driver.find_elements(strategy, locator)

        if len(elements) == 0:
            raise NoSuchElementException

        return elements

    def wait_till_text_appeared_in_element(self, text, strategy, locator, wait_time=None):
        if wait_time is None:
            wait = self.__wait
        else:
            wait = WebDriverWait(self.__driver, wait_time)

        try:
            text_found = wait.until(EC.text_to_be_present_in_element((strategy, locator), text))
            return text_found
        except (TimeoutException, NoSuchElementException):
            raise

    def wait_until_element_invisible(self, strategy, locator, wait_time=None):
        if wait_time is None:
            wait = self.__wait
        else:
            wait = WebDriverWait(self.__driver, wait_time)

        try:
            wait.until(EC.invisibility_of_element((strategy, locator)))
        except (TimeoutException, NoSuchElementException):
            raise

    def wait_until_corner_popup_message_is_hidden(self):
        try:
            for i in range(1, 10):
                self.wait_element_visible(*self.__CORNER_POPUP_MESSAGE, 1)
                time.sleep(1)
        except:
            pass

        # EC.invisibility_of_element doesn't work on CircleCI mahcines for some reason
        # self.wait_until_element_invisible(*self.__CORNER_POPUP_MESSAGE)
