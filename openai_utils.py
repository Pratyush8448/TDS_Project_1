import openai
import os

def determine_task(task_description):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate the task description into a function name."},
            {"role": "user", "content": f"Task: {task_description}. Respond with function name only."}
        ],
        api_key=os.environ["AIRPROXY_TOKEN"],
        timeout=20  # Ensuring execution completes within 20 seconds
    )
    return response["choices"][0]["message"]["content"]
