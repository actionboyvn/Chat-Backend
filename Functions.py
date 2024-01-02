import openai
from dotenv import load_dotenv
import os
import re

load_dotenv()

openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")

max_response_tokens = 100

system_prompt = f'''
Your task is to classify the user input according to the following intents.
Intent list:
1. get_response: For inquiries or requests for information
2. generate_image: For requests related to creating images
3. other: For any other kinds

Do not ask for additional context or information.
Return only one intent signature from the list following format: "Function: [intent]"
'''

def extract_signature(text):
    signatures = ['get_response', 'generate_image', 'other']

    pattern = r'\b(' + '|'.join(re.escape(sig) for sig in signatures) + r')\b'
    regex = re.compile(pattern)

    match = regex.search(text)

    return match.group(0) if match else 'other'

def get_function(prompt):
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}]
    
    response = openai.ChatCompletion.create(
        engine=os.getenv("OPENAI_API_DEPLOYMENT"),
        messages=messages,
        temperature=0.1,
        max_tokens=max_response_tokens,
    )

    returned_response = response['choices'][0]['message']['content']

    return extract_signature(returned_response)