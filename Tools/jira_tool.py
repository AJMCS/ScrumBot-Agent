import os
import requests
import json
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

def create_jira_tickets(tickets_json: str) -> str:
    """
    Create multiple Jira tickets from a JSON string containing ticket objects
    
    Args:
        tickets_json: JSON string containing an array of ticket objects
                      Each object should have: summary, description, project_key, issue_type (optional)
                      Example: '[{"summary": "Fix bug", "description": "Bug description", "project_key": "PROJ", "issue_type": "Bug"}]'
    
    Returns:
        str: Summary of all created tickets or error messages
    """
    try:
        # Parse the JSON string
        tickets = json.loads(tickets_json)
        
        # Ensure tickets is a list
        if not isinstance(tickets, list):
            tickets = [tickets]
        
        results = []
        successful_tickets = []
        failed_tickets = []
        
        for i, ticket_data in enumerate(tickets):
            # Extract ticket details with defaults
            summary = ticket_data.get("summary", f"Ticket {i+1}")
            description = ticket_data.get("description", "")
            project_key = ticket_data.get("project_key", "PROJ")
            issue_type = ticket_data.get("issue_type", "Task")
            
            # Create the ticket
            result = _create_single_ticket(summary, description, project_key, issue_type)
            
            if "Successfully created" in result:
                successful_tickets.append(result)
            else:
                failed_tickets.append(f"Ticket {i+1}: {result}")
        
        # Compile final result
        final_result = f"=== JIRA TICKET CREATION SUMMARY ===\n"
        final_result += f"Total tickets processed: {len(tickets)}\n"
        final_result += f"Successfully created: {len(successful_tickets)}\n"
        final_result += f"Failed: {len(failed_tickets)}\n\n"
        
        if successful_tickets:
            final_result += "=== SUCCESSFUL TICKETS ===\n"
            for ticket in successful_tickets:
                final_result += f"{ticket}\n\n"
        
        if failed_tickets:
            final_result += "=== FAILED TICKETS ===\n"
            for failure in failed_tickets:
                final_result += f"{failure}\n\n"
        
        return final_result
        
    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {str(e)}"
    except Exception as e:
        return f"Error processing tickets: {str(e)}"

def _create_single_ticket(summary: str, description: str, project_key: str, issue_type: str = "Task") -> str:
    """
    Helper function to create a single Jira ticket
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    auth = (JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Prepare the payload for creating a Jira issue
    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": issue_type
            }
        }
    }
    
    try:
        response = requests.post(url, headers=headers, auth=auth, json=payload)
        
        if response.status_code == 201:
            data = response.json()
            issue_key = data["key"]
            return f"Successfully created Jira ticket: {issue_key}\nSummary: {summary}\nProject: {project_key}\nType: {issue_type}"
        else:
            error_msg = f"Failed to create Jira ticket. Status code: {response.status_code}"
            try:
                error_data = response.json()
                if "errorMessages" in error_data:
                    error_msg += f"\nErrors: {', '.join(error_data['errorMessages'])}"
            except:
                error_msg += f"\nResponse: {response.text}"
            return error_msg
            
    except Exception as e:
        return f"Error creating Jira ticket: {str(e)}"

jira_tool = Tool(
    name="create_jira_tickets",
    func=create_jira_tickets,
    description="Creates multiple Jira tickets from a JSON string containing an array of ticket objects. Each object should have: summary, description, project_key, and optionally issue_type."
)