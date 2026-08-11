#AI agent with loop

import os
from litellm import completion
from typing import List,Dict

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY nicht gesetzt")

def generate_response(messages: List[Dict]) -> str:
    respone = completion(
        model= "openai/gpt-4o",
        messages= messages,
        max_tokens=1024,
    )

    return respone.choices[0].message.content

#Step 1: Construction the prompt 
prompt = agent_rules + memory 

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