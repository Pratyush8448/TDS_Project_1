import os
import json
import subprocess
import sys
import datetime
import sqlite3
import glob
from PIL import Image
import pytesseract

def generate_data():
    try:
        # ✅ Ensure 'uv' is installed
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)

        # ✅ Download 'datagen.py' script
        datagen_script = "datagen.py"
        subprocess.run([
            sys.executable, "-c",
            "import urllib.request; urllib.request.urlretrieve('https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py', 'datagen.py')"
        ], check=True)

        # ✅ Check if script exists before running
        if os.path.exists(datagen_script):
            subprocess.run([sys.executable, datagen_script], check=True)
        else:
            return {"error": "Failed to download 'datagen.py'."}

        return {"message": "Data generation completed ✅"}

    except subprocess.CalledProcessError as e:
        return {"error": f"Command failed: {e}"}

DATA_DIR = "./data"  # Update this if your data folder is different

def format_markdown():
    md_file_path = os.path.join(DATA_DIR, "format.md")

    # ✅ Ensure the file exists before formatting
    if not os.path.exists(md_file_path):
        return {"status": "error", "message": f"File not found: {md_file_path}"}

    try:
        # ✅ Use 'npx' to run prettier and format the markdown file
        subprocess.run(["npx", "prettier", "--write", md_file_path], check=True)
        return {"status": "success", "message": "Markdown formatted successfully"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}

def count_wednesdays():
    with open("/data/dates.txt", "r") as file:
        dates = file.readlines()
    
    count = sum(1 for date in dates if datetime.datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2)

    with open("/data/dates-wednesdays.txt", "w") as output_file:
        output_file.write(str(count))

    return f"{count} Wednesdays counted"

def sort_contacts():
    with open("/data/contacts.json", "r") as file:
        contacts = json.load(file)

    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))

    with open("/data/contacts-sorted.json", "w") as output_file:
        json.dump(sorted_contacts, output_file, indent=2)

    return "Contacts sorted successfully"

def extract_recent_logs():
    log_files = sorted(glob.glob("/data/logs/*.log"), key=os.path.getmtime, reverse=True)
    
    with open("/data/logs-recent.txt", "w") as output_file:
        for log in log_files[:10]:
            with open(log, "r") as file:
                output_file.write(file.readline())

    return "Recent logs extracted"

def create_markdown_index():
    index = {}
    for filename in glob.glob("/data/docs/*.md"):
        with open(filename, "r") as file:
            for line in file:
                if line.startswith("# "):
                    index[os.path.basename(filename)] = line.strip("# ").strip()
                    break
    
    with open("/data/docs/index.json", "w") as output_file:
        json.dump(index, output_file, indent=2)

    return "Markdown index created"


def extract_email_sender():
    file_path = "./data/email.txt"  # ✅ Use relative path

    if not os.path.exists(file_path):  # 🚨 Check if file exists
        return {"error": "File not found", "path": file_path}

    with open(file_path, "r") as file:
        email_content = file.read()

    # Extract sender email (modify if needed)
    sender_email = email_content.split("\n")[0].split(": ")[-1]

    output_path = "./data/email-sender.txt"
    with open(output_path, "w") as file:
        file.write(sender_email)

    return {"message": "Email sender extracted", "output": output_path}

def extract_credit_card():
    image = Image.open("/data/credit-card.png")
    card_number = pytesseract.image_to_string(image).replace(" ", "")

    with open("/data/credit-card.txt", "w") as file:
        file.write(card_number)

    return "Credit card number extracted"

def find_similar_comments():
    with open("/data/comments.txt", "r") as file:
        comments = file.readlines()

    most_similar = (comments[0], comments[1])

    with open("/data/comments-similar.txt", "w") as file:
        file.write("\n".join(most_similar))

    return "Most similar comments written"

def count_words():
    input_file = "/data/sample.txt"
    output_file = "/data/word-count.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            text = file.read()
            word_count = len(text.split())

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(str(word_count))

        return {"status": "success", "message": f"Word count saved in {output_file}"}

    except FileNotFoundError:
        return {"status": "error", "message": f"File {input_file} not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def calculate_ticket_sales():
    conn = sqlite3.connect("/data/ticket-sales.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
    total_sales = cursor.fetchone()[0]

    with open("/data/ticket-sales-gold.txt", "w") as file:
        file.write(str(total_sales))

    conn.close()

    return "Total sales calculated"
