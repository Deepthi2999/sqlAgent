from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client= Groq()

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "what is yur age?"
        }
    ]
)

print(response.choices[0].message.content)