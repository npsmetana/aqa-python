import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.create_issue_page import CreateIssuePage
from helpers.constants import *
import allure


@pytest.fixture(scope="function")
def get_driver():
    with allure.step("Prepare browser"):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                                      desired_capabilities=options.to_capabilities())
        driver.set_window_size(1920, 1080)
    yield driver
    with allure.step("Close browser"):
        driver.close()


@allure.title("Test login")
def test_login(get_driver):
    with allure.step("Test preparation"):
        driver = get_driver

        login_page = LoginPage(driver)
        main_page = MainPage(driver)

        login_page.open()

    with allure.step("Test login with wrong username and correct password"):
        login_page.login(BAD_USER, PASSWORD)
        assert login_page.is_login_failed()

    with allure.step("Test login with correct username and wrong password"):
        login_page.login(USER, BAD_PASSWORD)
        assert login_page.is_login_failed()

    with allure.step("Test login with correct username and password"):
        login_page.login(USER, PASSWORD)
        assert main_page.is_logged_in()


@allure.title("Test issue creation")
def test_create_issue(get_driver):
    with allure.step("Test preparation"):
        driver = get_driver

        login_page = LoginPage(driver)
        main_page = MainPage(driver)

        login_page.open()

        login_page.login(USER, PASSWORD)
        assert main_page.is_logged_in()

    with allure.step("Test issue creation - happy path"):
        create_issue_page = main_page.open_create_issue()
        create_issue_page.create_issue(ISSUE_SUMMARY)
        assert main_page.find_issue(ISSUE_SUMMARY)

    with allure.step("Test negative: issue creation with missing required field 'Summary'"):
        main_page.open_create_issue()
        assert create_issue_page.create_issue_no_summary()

    with allure.step("Test negative: issue creation with 'Summary' exceeding length limit"):
        main_page.open_create_issue()
        assert create_issue_page.create_issue_too_long_summary()


@allure.title("Test find issue")
def test_find_issue(get_driver):
    with allure.step("Test preparation"):
        driver = get_driver

        login_page = LoginPage(driver)
        main_page = MainPage(driver)

        login_page.open()

        login_page.login(USER, PASSWORD)
        assert main_page.is_logged_in()

    with allure.step("Test find existing issue"):
        assert main_page.find_issue(ISSUE_SUMMARY)

    with allure.step("Test find not existing issue"):
        assert main_page.find_issue_no_results("z" * 250)


@allure.title("Test update issue")
def test_update_issue(get_driver):
    with allure.step("Test preparation"):
        driver = get_driver

        login_page = LoginPage(driver)
        main_page = MainPage(driver)

        login_page.open()

        login_page.login(USER, PASSWORD)
        assert main_page.is_logged_in()

    with allure.step("Select issue for update"):
        main_page.find_issue(ISSUE_SUMMARY)

    with allure.step("Test update issue 'Assignee'"):
        assert main_page.update_issue_assignee(ISSUE_ASSIGNEE_UPD)

    with allure.step("Test update issue 'Summary'"):
        assert main_page.update_issue_summary(ISSUE_SUMMARY_UPD)

    with allure.step("Test update issue 'Priority'"):
        assert main_page.update_issue_priority(ISSUE_PRIORITY_UPD)

