from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class LoginPage(BasePage):
    __USER_NAME = (By.ID, "login-form-username")
    __USER_PASSWORD = (By.ID, "login-form-password")
    __LOGIN_BUTTON = (By.ID, "login-form-submit")
    __LOGIN_FAILED_MESSAGE = (By.CSS_SELECTOR, ".aui-message-error")

    @allure.step("Init 'LoginPage' object")
    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)
        self.__login_url = self.base_url + "/projects/WEBINAR/issues/?filter=allopenissues"
        self.__login_failed_url = self.base_url + "/login.jsp"

    @allure.step("Open Jira login URL")
    def open(self):
        self.driver.get(self.__login_url)

    @allure.step
    def login(self, user, password):
        self.set_element_text(user, *self.__USER_NAME)
        self.set_element_text(password, *self.__USER_PASSWORD)
        self.click_element(*self.__LOGIN_BUTTON)
        self.take_screen()

    @allure.step
    def is_login_failed(self):
        return self.is_page_opened_by_url(self.__login_failed_url)

