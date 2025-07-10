from langchain.tools import BaseTool
from typing import Optional, List
from JiraServices import create_jira_issue_flexible

class CreateJiraIssueTool(BaseTool):
    name: str = "create_jira_issue"
    description: str = "Creates a Jira issue in the specified project with flexible inputs."

    domain: str
    email: str
    api_token: str
    project_key: str

    def _run(
        self,
        summary: str,
        description: str,
        issue_type: str = "Task",
        story_points: Optional[int] = None,
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
        parent_key: Optional[str] = None,
        sprint_id: Optional[int] = None
    ) -> dict:
        return create_jira_issue_flexible(
            domain=self.domain,
            email=self.email,
            api_token=self.api_token,
            project_key=self.project_key,
            issue_type=issue_type,
            summary=summary,
            description=description,
            story_points=story_points,
            assignee=assignee,
            labels=labels,
            parent_key=parent_key,
            sprint_id=sprint_id
        )

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not supported yet.")
