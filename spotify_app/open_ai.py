from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv
# see also python-decouple

load_dotenv()

# openai.api_key = os.environ.get("OPEN_AI")
openai_api_key = os.getenv("OPENAI_KEY")
model = "gpt-3.5-turbo-0125"

client = OpenAI(
    api_key = openai_api_key
#   api_key=os.environ.get("OPENAI_API_KEY")    
)

def return_chatgpt_introduction(artist):
    message1 = [{
        "role": "user",
        "content": "Can you write a introduction paragraph about this " + artist + " , keep it simple and nice",
    }]

    chat_completion = client.chat.completions.create(
        messages=message1,
        model=model
    )
    return(chat_completion.choices[0].message.content)

print(return_chatgpt_introduction("Eminenm"))