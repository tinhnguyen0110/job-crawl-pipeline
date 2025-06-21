# processing/process_raw_jobs.py

import pandas as pd
import requests
import psycopg2
import json
import os
from datetime import datetime
import dateparser

from config.config_loader import load_config
from utils.logger import get_logger

logger = get_logger(__name__)

# ---------------------- PROMPT TEMPLATES ----------------------
PROMPT_TITLE = """
Task: From the job title string, extract:
1. job_title: The name of the job, excluding any seniority level or location/country prefix (like VN, SG, US, etc.).
2. seniority: One of the following levels if present: Intern, Fresher, Junior, Middle, Senior, Lead, Manager, Head, Principal, Director, Chief. Leave empty if no level is found.

Respond in JSON format like:
{{"job_title": "...", "seniority": "..."}}

Now, analyze the following title:
Input: {title}
"""

PROMPT_DESCRIPTION = """
Extract the following information from this job description:

- location
- salary
- job_description (short summary)
- job_requirements
- benefits

If any field is missing, leave it empty. Respond in JSON format like:
{{
  "location": "...",
  "salary": "...",
  "job_description": "...",
  "job_requirements": "...",
  "benefits": "..."
}}

Description:
{description}
"""

# ---------------------- UTILITY FUNCTIONS ----------------------

def fetch_raw_data(db_config, limit=10):
    try:
        conn = psycopg2.connect(**db_config)
        query = f"SELECT id, title, company, description, time_posted, date_crawled FROM raw_jobs ORDER BY id DESC LIMIT {limit};"
        df = pd.read_sql_query(query, conn)
        conn.close()
        logger.info(f"🔍 Đã lấy {len(df)} bản ghi từ database.")
        return df
    except Exception as e:
        logger.error(f"❌ Lỗi kết nối database: {e}")
        return pd.DataFrame()

def call_ollama(prompt: str, endpoint: str, model: str) -> dict:
    try:
        response = requests.post(
            endpoint,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        content = response.json()["response"]
        return json.loads(content.strip())
    except Exception as e:
        logger.error(f"❌ Lỗi gọi model '{model}' tại '{endpoint}': {e}")
        return {}

def parse_post_date(time_posted, date_crawled):
    if not time_posted or time_posted.strip().lower() in ["không rõ", ""]:
        return date_crawled
    parsed_date = dateparser.parse(
        time_posted,
        languages=['vi', 'en'],
        settings={'RELATIVE_BASE': datetime.combine(date_crawled, datetime.min.time())}
    )
    return parsed_date.strftime("%Y-%m-%d") if parsed_date else date_crawled

# --------------------------- MAIN -----------------------------

def process_raw_jobs():
    config = load_config()
    db_config = config["database"]
    ollama_cfg = config["ollama"]
    output_file = config["output"]["structured_csv_path"]

    logger.info("🚀 Bắt đầu xử lý job từ raw data.")
    df = fetch_raw_data(db_config)
    if df.empty:
        logger.warning("❗ Không có dữ liệu để xử lý.")
        return

    output_rows = []

    for _, row in df.iterrows():
        record_id = row['id']
        title = row['title']
        description = row['description']
        company = row['company']
        time_posted = row['time_posted']
        date_crawled = row['date_crawled']

        logger.info(f"🔄 Xử lý job ID {record_id}: {title} - {company}")

        title_prompt = PROMPT_TITLE.format(title=title)
        title_result = call_ollama(title_prompt, ollama_cfg["endpoint"], ollama_cfg["model"])
        job_title = title_result.get("job_title", "").strip()
        seniority = title_result.get("seniority", "").strip()

        desc_prompt = PROMPT_DESCRIPTION.format(description=description)
        desc_result = call_ollama(desc_prompt, ollama_cfg["endpoint"], ollama_cfg["model"])
        location = desc_result.get("location", "").strip()
        salary = desc_result.get("salary", "").strip()
        job_desc = desc_result.get("job_description", "").strip()
        requirements = desc_result.get("job_requirements", "").strip()
        benefits = desc_result.get("benefits", "").strip()

        post_date = parse_post_date(time_posted, date_crawled)

        output_rows.append({
            "id": record_id,
            "original_title": title,
            "company": company,
            "time_posted": time_posted,
            "date_crawled": date_crawled,
            "post_date": post_date,
            "job_title": job_title,
            "seniority": seniority,
            "location": location,
            "salary": salary,
            "job_description": job_desc,
            "job_requirements": requirements,
            "benefits": benefits,
            "model": ollama_cfg["model"],
        })

        logger.info(f"✅ Đã xử lý: {job_title} - {seniority} - {company}")

    pd.DataFrame(output_rows).to_csv(output_file, index=False)
    logger.info(f"📁 Đã lưu kết quả tại: {output_file}")

if __name__ == "__main__":
    process_raw_jobs()
