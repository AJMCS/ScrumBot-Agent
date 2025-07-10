import os
import requests
from dotenv import load_dotenv
from langchain.tools import Tool

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def get_jira_issue(issue_key: str) -> str:
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return f"Failed to fetch issue {issue_key}. Status code: {response.status_code}"

    data = response.json()
    fields = data["fields"]
    summary = fields["summary"]
    status = fields["status"]["name"]
    assignee = fields["assignee"]["displayName"] if fields["assignee"] else "Unassigned"

    return f"Issue {issue_key}: {summary}\nStatus: {status}\nAssignee: {assignee}"

jira_tool = Tool(
    name="get_jira_issues",
    func=get_jira_issue,
    description="Fetches jira issues"
)