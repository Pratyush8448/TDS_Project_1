import os
import json
import requests
import subprocess
import sqlite3
import duckdb
import markdown
import csv
import shutil
from fastapi import HTTPException
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
import speech_recognition as sr

# ✅ Security: Restrict access to /data/
DATA_DIR = "/data/"

def ensure_safe_path(filepath):
    """Ensure the given file path is inside the /data/ directory."""
    if not filepath.startswith(DATA_DIR):
        raise HTTPException(status_code=403, detail="Access outside /data/ is restricted.")

# 🚀 B3: Fetch data from an API and save it
def fetch_and_save_api_data(api_url, filename):
    ensure_safe_path(DATA_DIR + filename)
    response = requests.get(api_url)
    if response.status_code == 200:
        with open(DATA_DIR + filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        return {"status": "success", "message": f"Data saved to {filename}"}
    return {"status": "error", "message": f"Failed to fetch data (HTTP {response.status_code})"}

# 🚀 B4: Clone a git repo and make a commit
def clone_and_commit_repo(repo_url, commit_message):
    repo_path = os.path.join(DATA_DIR, "repo")
    ensure_safe_path(repo_path)

    if os.path.exists(repo_path):
        subprocess.run(["git", "-C", repo_path, "pull"], check=True)
    else:
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)

    with open(os.path.join(repo_path, "dummy.txt"), "w") as file:
        file.write("Test commit\n")

    subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
    subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)
    
    return {"status": "success", "message": "Commit created successfully"}

# 🚀 B5: Run a SQL query on SQLite or DuckDB
def run_sql_query(db_type, db_file, query):
    db_path = os.path.join(DATA_DIR, db_file)
    ensure_safe_path(db_path)

    if db_type == "sqlite":
        conn = sqlite3.connect(db_path)
    elif db_type == "duckdb":
        conn = duckdb.connect(db_path)
    else:
        return {"status": "error", "message": "Unsupported database type"}

    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()

    return {"status": "success", "result": result}

# 🚀 B6: Scrape data from a website
def scrape_website(url):
    response = requests.get(url)
    if response.status_code != 200:
        return {"status": "error", "message": "Failed to fetch website"}

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    
    with open(os.path.join(DATA_DIR, "scraped.txt"), "w", encoding="utf-8") as file:
        file.write(text)

    return {"status": "success", "message": "Website data saved"}

# 🚀 B7: Compress or resize an image
def compress_image(input_image, output_image, quality=50):
    input_path = os.path.join(DATA_DIR, input_image)
    output_path = os.path.join(DATA_DIR, output_image)
    ensure_safe_path(input_path)
    ensure_safe_path(output_path)

    image = Image.open(input_path)
    image.save(output_path, "JPEG", quality=quality)

    return {"status": "success", "message": f"Image saved as {output_image}"}

# 🚀 B8: Transcribe audio from an MP3 file
def transcribe_audio(mp3_file):
    mp3_path = os.path.join(DATA_DIR, mp3_file)
    ensure_safe_path(mp3_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(mp3_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    with open(os.path.join(DATA_DIR, "transcription.txt"), "w", encoding="utf-8") as file:
        file.write(text)

    return {"status": "success", "message": "Transcription saved"}

# 🚀 B9: Convert Markdown to HTML
def markdown_to_html(md_file, html_file):
    md_path = os.path.join(DATA_DIR, md_file)
    html_path = os.path.join(DATA_DIR, html_file)
    ensure_safe_path(md_path)
    ensure_safe_path(html_path)

    with open(md_path, "r", encoding="utf-8") as file:
        md_content = file.read()

    html_content = markdown.markdown(md_content)

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    return {"status": "success", "message": f"Converted {md_file} to {html_file}"}

# 🚀 B10: Write an API endpoint that filters a CSV file and returns JSON data
def filter_csv(csv_file, column_name, filter_value):
    csv_path = os.path.join(DATA_DIR, csv_file)
    ensure_safe_path(csv_path)

    filtered_rows = []
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[column_name] == filter_value:
                filtered_rows.append(row)

    return {"status": "success", "filtered_data": filtered_rows}
