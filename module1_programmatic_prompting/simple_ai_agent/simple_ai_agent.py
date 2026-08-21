#AI agent with loop

import json
import os
from litellm import completion
from typing import List,Dict

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY nicht gesetzt")

def extract_markdown_block(response: str, block_type: str = "json") -> str:
    """Extract code block from response"""

    if not '```' in response:
        return response

    code_block = response.split('```')[1].strip()

    if code_block.startswith(block_type):
        code_block = code_block[len(block_type):].strip()

    return code_block

def generate_response(prompt: List[Dict]) -> str:
    respone = completion(
        model= "openai/gpt-4o",
        messages= prompt,
        max_tokens=1024,
    )

    return respone.choices[0].message.content

def parse_action(response: str) -> Dict:
    """Parse the LLM response into a structured action dictionary."""
    try:
        response = extract_markdown_block(response, "action")
        response_json = json.loads(response)
        if "tool_name" in response_json and "args" in response_json:
            return response_json
        else:
            return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}}
    except json.JSONDecodeError:
        return {"tool_name": "error", "args": {"message": "Invalid JSON response. You must respond with a JSON tool invocation."}}

def list_files() -> List[str]:
    """List files in the current directory."""
    return os.listdir(".")

def read_file(file_name: str) -> str:
    """Read a file's contents."""
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except Exception as e:
        return f"Error: {str(e)}"
    
agent_rules = [{
    "role": "system",
    "content": """
 You are an AI agent that can perform tasks by using available tools.

 Available tools:
 - list_files() -> List[str]: List all files in the current directory.
 - read_file(file_name: str) -> str: Read the content of a file.
 - terminate(message: str): End the agent loop and print a summary to the user.

 If a user asks about files, list them before reading.

 Every response MUST have an action.
 Respond in this format:

 ```action
 {
    "tool_name": "insert tool_name",
    "args": {...fill in any required arguments here...}
    """
 }]

memory = [
    {"role": "user", "content": "What files are in this directory?"},
    {"role": "assistant", "content": "```action\n{\"tool_name\":\"list_files\",\"args\":{}}\n```"},
    {"role": "user", "content": "[\"file1.txt\", \"file2.txt\"]"}
 ]

iterations = 0
max_iterations = 10

while iterations < max_iterations: 
#Step 1: Construction the prompt 
 prompt = agent_rules + memory 

 #Step 2: Generate Response 
 response = generate_response(prompt)
 print(response)

 #Step 3: Parse the Response

 response = generate_response(prompt)
 print(response)

 #Step 4: Executing action

 action = parse_action(response)

 if action["tool_name"] == "list_files":
    result = {"result": list_files()}
 elif action["tool_name"] == "read_file":
    result = {"result": read_file(action["args"]["file_name"])}
 elif action["tool_name"] == "error":
    result = {"error": action["args"]["message"]}
 elif action["tool_name"] == "terminate":
    print(action["args"]["message"])
    break
 else:
    result = {"error":"Unknown action: "+action["tool_name"]}

#Step 5: Update memory

 memory.extend([
    {"role": "assistant", "content": response},
    {"role": "user", "content": json.dumps(result)}
 ])

 #Step 6: Decision to Continue
 if action["tool_name"] == "terminate":
    print(action["args"]["message"])
    break

 iterations += 1