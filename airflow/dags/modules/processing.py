import json
import logging
from datetime import datetime
import dateparser
import requests
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Table, Column, Integer, String, DateTime
from .database import JOBS_TABLE, PROCESSED_JOBS_TABLE
from sqlalchemy.dialects.postgresql import insert as pg_insert
import time
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
logger = logging.getLogger(__name__)

# ---------------------- PROMPT TEMPLATES ----------------------
PROMPT_TITLE = """
You are given a job title in either English or Vietnamese.

Extract the following:

1. "job_title": The main job title, excluding any location or country code prefix (e.g., "VN", "US", "SG").

2. "seniority": Based on your understanding, infer the most likely seniority level (such as Intern, Junior, Mid-level, Senior, Lead, Manager, Head, Director, etc.). If unclear, leave it empty.

You may infer synonyms (e.g., "Associate" = Junior, "Mid-level" = Middle, "Staff" = Senior).

Keep the original language in "job_title".

Respond only in JSON format:

{{"job_title": "...", "seniority": "..."}}

Now analyze this title:

Input: {title}
"""

PROMPT_DESCRIPTION = """
You are an AI specializing in parsing information from job postings.
Your task is to extract structured data fields from the job description text below.

### FIELD DEFINITIONS
- **location:** The workplace location.
- **salary:** The salary range (e.g., "Up to 2000 USD", "Negotiable").
- **job_description:** Describes the tasks and responsibilities the candidate will perform. Often found under headers like "Job Description", "Your Responsibilities".
- **job_requirements:** The skills, experience, and qualifications the candidate must have. Often found under headers like "Job Requirements", "Your Skills and Experience", "Qualifications".
- **benefits:** The perks and benefits the company offers. Often found under headers like "Benefits", "Perks", "Why you'll love working here".

### FORMATTING RULES
- Keep all text in its original language; do not translate.
- Extract text verbatim; do not summarize or rephrase.
- For `job_description`, `job_requirements`, and `benefits`: If there are multiple points, join them with a newline character (`\\n`). Remove any leading bullet symbols (e.g., '-', '*', '+').
- If information for any field is not found, return an empty string `""`.
- Respond only with a single, valid JSON object.

### TEXT TO PARSE
{description}
"""
# Endpoint giờ đây là DNS nội bộ của Kubernetes
# Dạng: http://<tên-service>.<tên-namespace>.svc.cluster.local:<port>/<path>
LITELLM_ENDPOINT = "http://litellm-service.platform-services:4000/chat/completions"
LITELLM_API_KEY = Variable.get("litellm-api-key", default_var="your_api_key_here")
VALID_MODELS = ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-1.5-pro-latest","gpt-4.1-nano","gpt-4.1-mini"]
if not LITELLM_API_KEY or LITELLM_API_KEY == "your_api_key_here":
    logger.warning("[LiteLLM] API key is missing or default is being used.")


# ---------------------- UTILITY FUNCTIONS ----------------------

def _call_litellm(prompt,model) -> dict:
    """
    Hàm gửi prompt đến LiteLLM Gateway, sử dụng cấu hình hardcode tạm thời.
    """
    try:

        headers = {"Authorization": f"Bearer {LITELLM_API_KEY}"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(LITELLM_ENDPOINT, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        llm_response_text = response.json()['choices'][0]['message']['content']
        return json.loads(llm_response_text)

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Lỗi mạng hoặc HTTP khi gọi model: {e}")
        raise ValueError(f"API call failed: {e}") from e
    except Exception as e:
        logger.error(f"❌ Lỗi không mong muốn trong hàm _call_litellm: {e}")
        raise ValueError(f"API call failed: {e}") from e

def call_with_model_fallback(prompt, primary_model):
    tried_models = set()
    models_to_try = [primary_model] + [m for m in VALID_MODELS if m != primary_model]

    for model in models_to_try:
        if model in tried_models:
            continue
        try:
            return _call_litellm(prompt, model)
        except Exception as e:
            tried_models.add(model)
            continue

    raise RuntimeError("❌ Tất cả các model đều lỗi.")

def _parse_post_date(time_posted, date_crawled_str):
    """Hàm tiện ích để parse ngày, cần chuyển đổi date_crawled_str thành datetime."""
    if not time_posted or time_posted.strip().lower() in ["không rõ", ""]:
        return date_crawled_str
    
    # Chuyển đổi date_crawled_str (là datetime object) về date object
    base_date = date_crawled_str.date() if isinstance(date_crawled_str, datetime) else date_crawled_str

    parsed_date = dateparser.parse(
        time_posted,
        languages=['vi', 'en'],
        settings={'RELATIVE_BASE': datetime.combine(base_date, datetime.min.time())}
    )
    return parsed_date if parsed_date else base_date


def process_jobs_and_update_db_callable(**kwargs):
    """
    Hàm chính được Airflow gọi, đã được tái cấu trúc hoàn chỉnh cho GKE.
    """
    params = kwargs.get("params", {})
    time_get_api = params.get("time_get_api", 10)  # Mặc định là 10 giây
    model_name_to_save = params.get("model_name") 
    

    if model_name_to_save not in VALID_MODELS:
        logger.warning(f"❌ Model '{model_name_to_save}' không hợp lệ. model mặc định là 'gemini-1.5-flash'")
        model_name_to_save = "gemini-1.5-flash"

    
    logger.info("Bắt đầu tác vụ xử lý dữ liệu thô bằng LLM...")

    # --- 1. Thiết lập kết nối Database ---
    ## TODO: Thay thế các giá trị hardcode này bằng Airflow Connection 'postgres_job_db'
    
    try:
        hook = PostgresHook(postgres_conn_id="cloud-sql")
        engine = hook.get_sqlalchemy_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1")  # Simple test query
            logger.info("[Postgres] Successfully connected to the Postgres database.")
    except Exception as e:
        logger.exception(f"[Postgres] Failed to connect to Postgres: {str(e)}")
    
    processed_count = 0
    
    try:
        with engine.connect() as connection:

            # --- 2. Lấy dữ liệu cần xử lý ---
            # Lấy 3 jobs chưa xử lý để làm việc trong một lần chạy
            select_query = text("SELECT id, title, company, description, time_posted, crawled_at FROM raw_jobs WHERE processed = FALSE;")
            jobs_to_process = connection.execute(select_query).mappings().all()

            if not jobs_to_process:
                logger.info("✅ Không có job mới nào để xử lý.")
                return "No new jobs to process."

            logger.info(f"Tìm thấy {len(jobs_to_process)} jobs để xử lý bằng LLM.")
            
            # --- 3. Xử lý từng Job ---
            for job in jobs_to_process:
                job_id = job['id']
                logger.info(f"🔄 Đang xử lý job ID {job_id}: {job['title']}")
                try:
                    # Gọi LLM để xử lý title và description
                    title_result = call_with_model_fallback(PROMPT_TITLE.format(title=job['title']), model_name_to_save)
                    desc_result = call_with_model_fallback(PROMPT_DESCRIPTION.format(description=job['description']), model_name_to_save)
                    # Tính toán ngày đăng
                    post_date = _parse_post_date(job['time_posted'], job['crawled_at'])

                    # Tổng hợp dữ liệu cuối cùng
                    final_data = {
                        "raw_job_id": job_id,
                        "job_title": title_result.get("job_title"),
                        "seniority": title_result.get("seniority"),
                        "company": job['company'],
                        "location": desc_result.get("location"),
                        "salary": desc_result.get("salary"),
                        "job_description": desc_result.get("job_description"),
                        "job_requirements": desc_result.get("job_requirements"),
                        "benefits": desc_result.get("benefits"),
                        "date_posted": post_date,
                        "model": model_name_to_save
                    }

                    # Bắt đầu transaction để đảm bảo toàn vẹn dữ liệu
                    with connection.begin() as transaction:
                        try:
                            # 4. INSERT vào bảng processed_jobs
                            # SỬA Ở ĐÂY: Dùng pg_insert() thay vì .insert()
                            insert_stmt = pg_insert(PROCESSED_JOBS_TABLE).values(final_data)

                            # Phần còn lại giữ nguyên, bây giờ nó sẽ hoạt động
                            upsert_stmt = insert_stmt.on_conflict_do_update(
                                index_elements=['raw_job_id'],
                                set_={
                                    # Cập nhật tất cả các cột trừ cột id và raw_job_id
                                    col.name: getattr(insert_stmt.excluded, col.name) 
                                    for col in PROCESSED_JOBS_TABLE.c 
                                    if col.name not in ['id', 'raw_job_id']
                                }
                            )
                            connection.execute(upsert_stmt)

                            # 5. UPDATE cờ trong bảng jobs (giữ nguyên)
                            update_stmt = JOBS_TABLE.update().where(JOBS_TABLE.c.id == job_id).values(processed=True)
                            connection.execute(update_stmt)

                            logger.info(f"✅ Đã xử lý thành công job ID: {job_id}")
                            time.sleep(time_get_api)  # Giả lập thời gian xử lý
                            processed_count += 1
                        except Exception as e:
                            logger.error(f"❌ Lỗi khi xử lý job ID {job_id}. Lỗi: {e}. Bỏ qua job này.")
                            continue
                except Exception as e:
                    logger.error(f"❌ Lỗi không xác định trong quá trình xử lý job ID {job_id}: {e}", exc_info=True)
                    continue 
                
    except SQLAlchemyError as e:
        logger.error(f"❌ Lỗi kết nối hoặc thực thi SQL: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"❌ Lỗi không xác định trong quá trình xử lý: {e}", exc_info=True)
        raise

    return f"Hoàn tất. Đã xử lý thành công {processed_count}/{len(jobs_to_process)} jobs."