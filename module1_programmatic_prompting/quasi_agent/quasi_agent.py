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

what_do_you_want = input("What can I create for you?")

# Ask the LLM what you want
messages = [
    {"role": "system", "content": "You are an Software Engineer, who programs python functions"},
    {"role": "user", "content": what_do_you_want}
]

respone = generate_response(messages)
print(respone)

next_input = input("What should we do next ?")

messages = [
    {"role": "system", "content": "You are an Software Engineer, who programs python functions" },
    {"role": "user", "content": what_do_you_want},
    {"role": "assistant", "content": respone},
    {"role": "user", "content": next_input}
]

respone2 = generate_response(messages)
print(respone2)