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

logger = logging.getLogger(__name__)

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

def _call_litellm(prompt,model) -> dict:
    """
    Hàm gửi prompt đến LiteLLM Gateway, sử dụng cấu hình hardcode tạm thời.
    """
    try:
        # THAY ĐỔI CHO GKE 1: Cấu hình hardcode
        # Endpoint giờ đây là DNS nội bộ của Kubernetes
        # Dạng: http://<tên-service>.<tên-namespace>.svc.cluster.local:<port>/<path>
        endpoint = "http://litellm-proxy-deployment.model-serving:4000/chat/completions" # <-- THAY THẾ BẰNG TÊN SERVICE & NAMESPACE CỦA BẠN
        api_key = "sk-SlN5E-XYkuaI02FUeZxV9g" # <-- ## TODO: Chuyển vào Airflow Connection sau này

        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(endpoint, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        llm_response_text = response.json()['choices'][0]['message']['content']
        return json.loads(llm_response_text)

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Lỗi mạng hoặc HTTP khi gọi model: {e}")
        raise ValueError(f"API call failed: {e}") from e
    except Exception as e:
        logger.error(f"❌ Lỗi không mong muốn trong hàm _call_litellm: {e}")
        raise ValueError(f"API call failed: {e}") from e

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
    logger.info("Bắt đầu tác vụ xử lý dữ liệu thô bằng LLM...")

    # --- 1. Thiết lập kết nối Database ---
    ## TODO: Thay thế các giá trị hardcode này bằng Airflow Connection 'postgres_job_db'
    db_user = "postgres"
    db_pass = "123456"
    db_name = "job_db"
    db_host = "127.0.0.1"
    db_port = 5432

    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url)
    
    model_name_to_save = "gemini-1.5-flash" # TODO: Lấy từ Airflow Variable sau này

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
                    title_result = _call_litellm(PROMPT_TITLE.format(title=job['title']), model_name_to_save)
                    desc_result = _call_litellm(PROMPT_DESCRIPTION.format(description=job['description']), model_name_to_save)
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