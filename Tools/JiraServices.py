import requests
from requests.auth import HTTPBasicAuth
import json

def set_story_point_estimate(domain, email, api_token, issue_key, story_points):
    """
    Sets the Story point estimate for a Jira issue (Team-Managed projects only).

    Args:
        domain (str): Your Jira domain.
        email (str): Your Jira email.
        api_token (str): Your Jira API token.
        issue_key (str): The Jira issue key, e.g., "SCRUM-7".
        story_points (int): The story point estimate value to set.

    Returns:
        dict: API response or success message.
    """
    url = f"https://{domain}/rest/api/3/issue/{issue_key}"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    field_id = "customfield_10043"

    payload = {
        "fields": {
            field_id: story_points
        }
    }

    response = requests.put(url, headers=headers, auth=auth, data=json.dumps(payload))

    if response.status_code != 204:
        raise Exception(f"Failed to update story points: {response.status_code} {response.text}")

    return {"status": "Story points updated", "issue": issue_key, "story_points": story_points}


def create_jira_issue_flexible(
    domain,
    email,
    api_token,
    project_key,
    issue_type,
    summary,
    description=None,
    assignee=None,
    labels=None,
    parent_key=None,
    sprint_id=None,
    story_points=None
):
    """
    Creates a Jira issue and optionally sets Story point estimate after creation.

    Returns:
        dict: Created issue response.
    """
    url = f"https://{domain}/rest/api/3/issue"
    auth = HTTPBasicAuth(email, api_token)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    fields = {
        "project": {"key": project_key},
        "summary": summary,
        "issuetype": {"name": issue_type},
    }

    if description:
        fields["description"] = description
    if labels:
        fields["labels"] = labels
    if assignee:
        fields["assignee"] = {"id": assignee}
    if parent_key:
        fields["parent"] = {"key": parent_key}

    payload = {"fields": fields}

    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))

    if response.status_code not in [200, 201]:
        raise Exception(f"Error {response.status_code}: {response.text}")

    issue = response.json()
    issue_key = issue.get("key")

    if story_points is not None:
        set_story_point_estimate(domain, email, api_token, issue_key, story_points)

    return issue
