from helpers.constants import *
import allure


class Data2Json(object):
    @staticmethod
    @allure.step("Get 'Authentication' JSON data")
    def auth(username, password):
        return {
            "username": username,
            "password": password
        }

    @staticmethod
    @allure.step("Get 'Create issue' JSON data")
    def create_issue(summary, priority):
        description = "Description of '" + summary + "'"
        return {
            "fields": {
                "project": {
                    "key": PROJECT_NAME
                },
                "issuetype": {
                    "name": ISSUE_TYPE
                },
                "summary": summary,
                "description": description,
                "priority": {
                    "name": priority
                }
            }
        }

    @staticmethod
    @allure.step("Get 'Search issue' JSON data")
    def search_issue(summary):
        return {
            "jql": "summary ~ " + "\"" + summary + "\"",
            "maxResults": 15,
            "fields": [
                "summary",
                "description",
                "project",
                "priority",
                "assignee"
            ],
            "startAt": 0
        }

    @staticmethod
    @allure.step("Get 'Update issue' JSON data")
    def update_issue(field, value):
        if field == "assignee":
            return {
                "fields": {
                    "assignee": {
                        "name": value
                    }
                }
            }
        elif field == "summary":
            return {
                "fields": {
                    "summary": value
                }
            }
        elif field == "priority":
            return {
                "fields": {
                    "priority": {
                        "name": value
                    }
                }
            }
        else:
            return {
                "fields": {}
            }

    @staticmethod
    @allure.step("Get specified field value")
    def get_field_value(issue, field):
        if field == "assignee":
            return issue["fields"]["assignee"]["name"]
        elif field == "summary":
            return issue["fields"]["summary"]
        elif field == "priority":
            return issue["fields"]["priority"]["name"]
        else:
            return None
