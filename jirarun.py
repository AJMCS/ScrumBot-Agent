from CreateJiraIssueTool import CreateJiraIssueTool
import requests
from requests.auth import HTTPBasicAuth

# Prepare your Jira details:
jira_tool = CreateJiraIssueTool(
    domain="cesarhackathon.atlassian.net",
    email="your-email@example.com",
    api_token="your-api-token",
    project_key="SCRUM"
)

# ✅ Here's your full test call with every field set:
result = jira_tool._run(
    summary="AI Assistant Implementation",
    description={
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "This is a full test issue with every supported field populated."}
                ]
            }
        ]
    },
    issue_type="Story",                  # Must be "Story" for Story Points
    story_points=8,                      # Will be set in second call
    assignee="JIRA_ACCOUNT_ID",          # You must use the Account ID (not email) here
    labels=["automation", "test", "AI"],
    parent_key=None,                     # Only needed for sub-tasks; can be None
    sprint_id=None                       # Optional: Team-Managed projects usually manage sprints differently
)

print("✅ Issue Created:", result)
