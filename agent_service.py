import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from todo_service import (
    add_task,
    get_tasks,
    update_task,
    delete_task
)

FUNCTIONS = {
        "add_task": add_task,
        "get_tasks": get_tasks,
        "update_task": update_task,
        "delete_task": delete_task
}   

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task."
                    },
                    "description": {
                        "type": "string",
                        "description": "The description of the task."
                    },
                    "task_type": {
                        "type": "string",
                        "description": "Task category."
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date."
                    },
                    "status": {
                        "type": "string",
                        "description": "Task status."
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "Return all tasks. You may filter by status or task type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "description": "Filter by task status."
                            },
                            "type": {
                                "type": "string",
                                "description": "Filter by task type."
                            }
                        }
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "Task id."
                    },
                    "title": {
                        "type": "string",
                        "description": "New title."
                    },
                    "description": {
                        "type": "string",
                        "description": "New description."
                    },
                    "task_type": {
                        "type": "string",
                        "description": "New task type."
                    },
                    "start_date": {
                        "type": "string",
                        "description": "New start date."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "New end date."
                    },
                    "status": {
                        "type": "string",
                        "description": "New status."
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "Task id."
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]

    

def agent(query):
    messages = [
    {
        "role": "system",
        "content": (
            "You are a task management assistant. "
            "Always use the provided functions when the user wants "
            "to add, update, delete or retrieve tasks. "
            "Never invent task data."
        )
    },
    {
        "role": "user",
        "content": query
    }
    ]
   
    response = client.chat.completions.create(
    model="gpt-5",
    messages=messages,
    tools=tools
    )

    tool_calls = response.choices[0].message.tool_calls

# אם המודל לא ביקש לקרוא לפונקציה
    if not tool_calls:
        return response.choices[0].message.content

    messages.append(response.choices[0].message)

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        function = FUNCTIONS[function_name]
        result = function(**args)

    messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result, ensure_ascii=False)
    })

    final_response = client.chat.completions.create(
        model="gpt-5",
        messages=messages,
        tools=tools
    )
    print(result)

    return final_response.choices[0].message.content