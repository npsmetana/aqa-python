import requests
import pytest
import json
from helpers.json_fixtures import *
import allure
from allure_commons.types import AttachmentType

issue_keys = []
flaky_test_pass_flag = False


@pytest.mark.flaky(reruns=2, reruns_delay=2)
@allure.title("Test re-run flaky test")
def test_passes_on_second_run():
    global flaky_test_pass_flag
    with allure.step("This time test will pass: " + str(flaky_test_pass_flag)):
        pass_flag = flaky_test_pass_flag
        flaky_test_pass_flag = True
        allure.attach(str(pass_flag), name="flaky_test_pass_flag", attachment_type=AttachmentType.TEXT)
        assert pass_flag


@pytest.mark.parametrize('user,password,code',
                         [
                             (USER, BAD_PASSWORD, 401),
                             (BAD_USER, PASSWORD, 401),
                             (USER, PASSWORD, 200)
                         ])
@allure.title("Test API authentication")
def test_api_login(user, password, code):
    with allure.step("Test preparation"):
        url = BASE_API_URL + 'auth/1/session'
        auth_data = Data2Json.auth(user, password)

    with allure.step("Authenticate with username/password '" + user + " / " + password + "'"):
        r = requests.post(url, json=auth_data, headers=REQ_API_HEADERS)

    with allure.step("Check authentication"):
        allure.attach(str(r.status_code) + " / " + str(code), name="Authentication request status code (current/expected)",
                      attachment_type=AttachmentType.TEXT)
    assert r.status_code == code


@pytest.mark.parametrize('summary,priority,code,err_msg',
                         [
                             (BASE_ISSUE_SUMMARY + " 1", "Lowest", 201, ""),
                             (BASE_ISSUE_SUMMARY + " 2", "Low", 201, ""),
                             (BASE_ISSUE_SUMMARY + " 3", "Medium", 201, ""),
                             (BASE_ISSUE_SUMMARY + " 4", "High", 201, ""),
                             (BASE_ISSUE_SUMMARY + " 5", "Highest", 201, ""),
                             ("", "Blocker", 400, "You must specify a summary of the issue."),
                             ("z" * 256, "Blocker", 400, "Summary must be less than 255 characters.")
                         ])
@allure.title("Test API create issue")
def test_api_create_issue(summary, priority, code, err_msg):
    with allure.step("Test preparation"):
        url = BASE_API_URL + 'api/2/issue'
        new_issue = Data2Json.create_issue(summary, priority)

    with allure.step("Create issue with summary '" + summary + "' and priority '" + priority + "'"):
        r = requests.post(url, json=new_issue, auth=(USER, PASSWORD), headers=REQ_API_HEADERS)
        reply = json.loads(r.text)

    with allure.step("Check issue"):
        allure.attach(str(r.status_code) + " / " + str(code), name="Create issue request status code (current/expected)",
                      attachment_type=AttachmentType.TEXT)
        if r.status_code == 201:
            issue_keys.append(reply["key"])
        else:
            allure.attach("'" + reply["errors"]["summary"] + "' / '" + err_msg + "'",
                          name="Issue creation failed with error message (current/expected)",
                          attachment_type=AttachmentType.TEXT)
        assert r.status_code == code \
               and err_msg in r.text


@pytest.mark.parametrize('search_summary,num_found',
                         [
                             (BASE_ISSUE_SUMMARY + " 4", 1),
                             (BASE_ISSUE_SUMMARY, 5),
                             ("z" * 250, 0)
                         ])
@allure.title("Test API find issue")
def test_api_search_issue(search_summary, num_found):
    with allure.step("Test preparation"):
        url = BASE_API_URL + 'api/2/search'
        search_issue = Data2Json.search_issue(search_summary)

    with allure.step("Search for issue with summary '" + search_summary + "'"):
        r = requests.post(url, json=search_issue, auth=(USER, PASSWORD), headers=REQ_API_HEADERS)
        reply = json.loads(r.text)

    with allure.step("Check search"):
        allure.attach(str(r.status_code) + " / 200", name="Search issue request status code (current/expected)",
                      attachment_type=AttachmentType.TEXT)
        really_found = reply["total"]
        allure.attach(str(really_found) + " / " + str(num_found), name="Number of found issue(s) (current/expected)",
                      attachment_type=AttachmentType.TEXT)
        assert r.status_code == 200 \
               and really_found == num_found


@pytest.mark.parametrize('update_field,new_value',
                         [
                             ("summary", BASE_ISSUE_SUMMARY_UPDATED),
                             ("assignee", USER),
                             ("priority", "Blocker")
                         ])
@allure.title("Test API update issue")
def test_api_update_issue(update_field, new_value):
    with allure.step("Test preparation"):
        issue_key = issue_keys[0]
        url = BASE_API_URL + 'api/2/issue/' + issue_key
        update_issue = Data2Json.update_issue(update_field, new_value)

    with allure.step("Update issue '" + issue_key + "' field '" + update_field + "' with value '" + new_value + "'"):
        r_update = requests.put(url, json=update_issue, auth=(USER, PASSWORD), headers=REQ_API_HEADERS)

    with allure.step("Get issue '" + issue_key + "' after update"):
        r_get = requests.get(url, auth=(USER, PASSWORD), headers=REQ_API_HEADERS)
        reply_get = json.loads(r_get.text)

    with allure.step("Check update"):
        allure.attach(str(r_update.status_code) + " / 204", name="Update issue request status code (current/expected)",
                      attachment_type=AttachmentType.TEXT)
        allure.attach(str(r_get.status_code) + " / 200", name="Get issue request status code (current/expected)",
                      attachment_type=AttachmentType.TEXT)
        current_value = Data2Json.get_field_value(reply_get, update_field)
        allure.attach(current_value + " / " + new_value, name="Field value (current/expected)",
                      attachment_type=AttachmentType.TEXT)
        assert r_update.status_code == 204 \
               and r_get.status_code == 200 \
               and current_value == new_value


@allure.title("Test API cleanup")
def test_api_cleanup():
    for issue_key in issue_keys:
        with allure.step("Delete issue " + issue_key):
            url = BASE_API_URL + 'api/2/issue/' + str(issue_key)
            r = requests.delete(url, auth=(USER, PASSWORD), headers=REQ_API_HEADERS)
            allure.attach(str(r.status_code), name="Delete request status code", attachment_type=AttachmentType.TEXT)
