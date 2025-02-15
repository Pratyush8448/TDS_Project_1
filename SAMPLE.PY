import openai
import os

openai.api_key = os.getenv("AIPROXY_TOKEN")

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, AI Proxy! Can you respond?"}]
    )
    print(response["choices"][0]["message"]["content"])
except Exception as e:
    print("Error:", e)
