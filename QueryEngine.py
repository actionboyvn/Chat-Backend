import tiktoken
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")

max_response_tokens = 1000
token_limit = 4096
conversation = []

def num_tokens_from_messages(messages):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += -1
    num_tokens += 2
    return num_tokens

async def query(conv):
    messages = []
    messages.extend(conv["conversation"])

    user_query = messages[-1]["content"]

    messages.append({"role": "user", "content": user_query})
    
    conv_history_tokens = num_tokens_from_messages(messages)

    while conv_history_tokens + max_response_tokens >= token_limit:
        del messages[1]
        conv_history_tokens = num_tokens_from_messages(messages)

    response = await openai.ChatCompletion.acreate(
        engine=os.getenv("OPENAI_API_DEPLOYMENT"),
        messages=messages,
        temperature=0.5,
        max_tokens=max_response_tokens,
    )

    returned_response = response['choices'][0]['message']['content']
    
    return {"response": returned_response}