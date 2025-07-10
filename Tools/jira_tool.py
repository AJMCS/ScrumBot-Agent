from langchain.tools import Tool

def get_jira_issues(): 
    pass


jira_tool = Tool(
    name="get_jira_issues",
    func=get_jira_issues,
    description="Fetches jira issuess"
)