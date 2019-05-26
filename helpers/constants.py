from time import strftime, localtime

USER = "NicolaySmetana"
PASSWORD = "NicolaySmetana"

BAD_USER = "NicolaySmetana22"
BAD_PASSWORD = "NicolaySmetana33"

TIME_STAMP = strftime("%Y%m%d_%H%M%S", localtime())
ISSUE_SUMMARY = "NSmetana test issue" + " " + str(TIME_STAMP)
ISSUE_PRIORITY_UPD = "Blocker"
ISSUE_ASSIGNEE_UPD = "NicolaySmetana"
ISSUE_SUMMARY_UPD = ISSUE_SUMMARY + " UPDATED"

BASE_API_URL = "https://jira.hillel.it/rest/"
REQ_API_HEADERS = {'Content-Type': 'application/json'}
BASE_ISSUE_SUMMARY = "NSmetana test API issue"
BASE_ISSUE_SUMMARY_UPDATED = BASE_ISSUE_SUMMARY + " UPDATED"
PROJECT_NAME = "WEBINAR"
ISSUE_TYPE = "Bug"