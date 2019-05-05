import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.create_issue_page import CreateIssuePage
from helpers.constants import *


@pytest.fixture(scope="function")
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                              desired_capabilities=options.to_capabilities())
    driver.set_window_size(1920, 1080)
    yield driver
    driver.close()


def test_login(get_driver):
    driver = get_driver

    login_page = LoginPage(driver)
    main_page = MainPage(driver)

    login_page.open()

    login_page.login(BAD_USER, PASSWORD)
    assert login_page.is_login_failed()

    login_page.login(USER, BAD_PASSWORD)
    assert login_page.is_login_failed()

    login_page.login(USER, PASSWORD)
    assert main_page.is_logged_in()


def test_create_issue(get_driver):
    driver = get_driver

    login_page = LoginPage(driver)
    main_page = MainPage(driver)

    login_page.open()

    login_page.login(USER, PASSWORD)
    assert main_page.is_logged_in()

    create_issue_page = main_page.open_create_issue()
    create_issue_page.create_issue(ISSUE_SUMMARY)
    assert main_page.find_issue(ISSUE_SUMMARY)

    main_page.open_create_issue()
    assert create_issue_page.create_issue_no_summary()

    main_page.open_create_issue()
    assert create_issue_page.create_issue_too_long_summary()


def test_find_issue(get_driver):
    driver = get_driver

    login_page = LoginPage(driver)
    main_page = MainPage(driver)

    login_page.open()

    login_page.login(USER, PASSWORD)
    assert main_page.is_logged_in()

    assert main_page.find_issue(ISSUE_SUMMARY)

    assert main_page.find_issue_no_results("z" * 250)


def test_update_issue(get_driver):
    driver = get_driver

    login_page = LoginPage(driver)
    main_page = MainPage(driver)

    login_page.open()

    login_page.login(USER, PASSWORD)
    assert main_page.is_logged_in()

    main_page.find_issue(ISSUE_SUMMARY)

    assert main_page.update_issue_assignee(ISSUE_ASSIGNEE_UPD)

    assert main_page.update_issue_summary(ISSUE_SUMMARY_UPD)

    assert main_page.update_issue_priority(ISSUE_PRIORITY_UPD)

