from prompts.test_prompts import test_prompt
from tools.jira_tool import create_jira_tickets
import openai
import os
import json

client = openai.OpenAI(
    api_key=os.getenv("OXEN_API_KEY"),
    base_url="https://hub.oxen.ai/api"
)

# Define the tool in OpenAI function calling format
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_jira_tickets",
            "description": "Creates multiple Jira tickets from a JSON string containing an array of ticket objects. Each object should have: summary, description, project_key, and optionally issue_type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tickets_json": {
                        "type": "string",
                        "description": "JSON string containing an array of ticket objects. Each object should have: summary, description, project_key, and optionally issue_type."
                    }
                },
                "required": ["tickets_json"]
            }
        }
    }
]

try:
    response = client.chat.completions.create(
        model="openai:gpt-4o-mini",
        messages=[{"role": "user", 
                   "content": "Please give me a list of jira issues from the following transcript in JSON format where each json object is a seperate ticket:" + test_prompt()}],
        tools=tools,
        tool_choice="auto"
    )
    
    print("=== Full Response Debug ===")
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")
    print(f"Has choices: {hasattr(response, 'choices')}")
    if hasattr(response, 'choices'):
        print(f"Choices length: {len(response.choices) if response.choices else 'None'}")
    
    # Handle the response
    if response and response.choices:
        message = response.choices[0].message
        
        # Check if the AI wants to call a function
        if message.tool_calls:
            # Get the function call
            tool_call = message.tool_calls[0]
            
            if tool_call.function.name == "create_jira_tickets":
                # Parse the arguments
                args = json.loads(tool_call.function.arguments)
                tickets_json = args["tickets_json"]
                
                # Execute the function
                result = create_jira_tickets(tickets_json)
                
                print("=== AI Response ===")
                print(message.content)
                print("\n=== Function Call ===")
                print(f"Function: {tool_call.function.name}")
                print(f"Arguments: {tickets_json}")
                print("\n=== Function Result ===")
                print(result)
            else:
                print("Unknown function called:", tool_call.function.name)
        else:
            # No function call, just print the response
            print("=== AI Response ===")
            print(message.content)
    else:
        print("No valid response received from API")
        print(f"Response object: {response}")

except Exception as e:
    print(f"Error occurred: {str(e)}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()