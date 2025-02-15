from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from TASKS import (
    generate_data, format_markdown, count_wednesdays, sort_contacts,
    extract_recent_logs, create_markdown_index, extract_email_sender,
    extract_credit_card, find_similar_comments, calculate_ticket_sales
)
from phase2_tasks import (
    fetch_and_save_api_data, clone_and_commit_repo, run_sql_query,
    scrape_website, compress_image, transcribe_audio,
    markdown_to_html, filter_csv
)
from openai_utils import determine_task

app = FastAPI()

# ✅ Use AI Proxy Token (Set in Environment Variables)
openai.api_key = os.getenv("AIPROXY_TOKEN")

class TaskRequest(BaseModel):
    task: str

# 🔥 TASK MAPPING DICTIONARY
TASK_MAPPING = {
    # 🔹 Phase A Tasks
    "install uv": generate_data,
    "generate data": generate_data,
    "format markdown": format_markdown,
    "format.md": format_markdown,
    "count wednesdays": count_wednesdays,
    "count days": count_wednesdays,
    "sort contacts": sort_contacts,
    "extract logs": extract_recent_logs,
    "recent logs": extract_recent_logs,
    "index markdown": create_markdown_index,
    "create index": create_markdown_index,
    "extract email sender": extract_email_sender,
    "email.txt": extract_email_sender,
    "extract credit card": extract_credit_card,
    "credit-card.png": extract_credit_card,
    "find similar comments": find_similar_comments,
    "comments.txt": find_similar_comments,
    "total sales": calculate_ticket_sales,
    "gold tickets": calculate_ticket_sales,

    # 🔹 Phase B Tasks
    "fetch api data": fetch_and_save_api_data,
    "clone repo": clone_and_commit_repo,
    "run sql": run_sql_query,
    "scrape website": scrape_website,
    "compress image": compress_image,
    "transcribe audio": transcribe_audio,
    "convert markdown": lambda: markdown_to_html("data/input.md", "data/output.html"),
    "filter csv": filter_csv,
}

# 🔒 Security Constraints (B1 & B2)
def is_safe_path(filepath: str) -> bool:
    """
    Ensures the file is within the allowed `/data/` directory.
    Prevents deletion of any files.
    """
    safe_dir = os.path.abspath("./data")
    requested_path = os.path.abspath(filepath)
    
    return requested_path.startswith(safe_dir)

@app.post("/run")
async def run_task(request: TaskRequest):
    """
    Runs a task based on the user's plain-English instructions.
    """
    task = request.task.lower()
    print(f"Received Task: {task}")  # ✅ Debugging log

    try:
        # 🔥 TASK MAPPING IMPLEMENTATION 🔥
        for key in TASK_MAPPING:
            if key in task:
                return TASK_MAPPING[key]()

        # 🤖 If no direct match, use GPT-4o-Mini via AI Proxy
        function_name = determine_task(task)
        if function_name in TASK_MAPPING:
            return TASK_MAPPING[function_name]()

        print(f"Unrecognized Task: {task}")  # ✅ Debugging log
        return {"status": "error", "message": "Task not recognized."}

    except Exception as e:
        print(f"Error: {str(e)}")  # ✅ Debugging log
        raise HTTPException(status_code=500, detail=str(e))
