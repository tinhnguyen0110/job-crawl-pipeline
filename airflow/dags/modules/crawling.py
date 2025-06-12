import os
import json
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeoutError
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from .database import METADATA, JOBS_TABLE

logger = logging.getLogger(__name__)

def _close_popups(page: Page):
    popup_close_selectors = [".dismiss", "button[aria-label='Close']"]
    for selector in popup_close_selectors:
        try:
            popup_button = page.locator(selector).first
            if popup_button.is_visible(timeout=500):
                logger.info(f"Phát hiện và đóng pop-up với selector: '{selector}'")
                popup_button.click(timeout=2000)
                page.wait_for_timeout(500)
        except PlaywrightTimeoutError:
            pass
        except Exception as e:
            logger.warning(f"Lỗi không mong đợi khi cố gắng đóng pop-up '{selector}': {e}")

def safe_click(page, job_card):

    # Dọn dẹp pop-up trước khi click
    _close_popups(page)
    
    # Thực hiện hành động click chính
    logger.info("Thực hiện click vào job card...")
    job_card.click()
    
    # Dọn dẹp pop-up một lần nữa sau khi click
    _close_popups(page)


def crawl_jobstreet_to_local_callable(**kwargs):
    logical_date = kwargs["ds"]
    run_id = kwargs["run_id"]
    params = kwargs.get("params", {})
    start_url = params.get("start_url")
    if not start_url:
        raise ValueError("Không tìm thấy 'start_url' trong params của DAG.")

    safe_run_id = run_id.replace(":", "_").replace("+", "_")
    output_dir = f"/opt/airflow/data/{logical_date}"
    output_filename = f"{safe_run_id}.json"
    output_file_path = os.path.join(output_dir, output_filename)

    logger.info(f"🚀 Bắt đầu crawl từ URL: {start_url}")
    logger.info(f"📁 File output sẽ được lưu tại: {output_file_path}")
    os.makedirs(output_dir, exist_ok=True)

    scraped_data = []
    browser = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(start_url)
            base_url = "https://www.jobstreet.vn"
            page_num = 1
            
            while page_num <= 2:
                logger.info(f"🔄 Đang xử lý trang {page_num} tại URL: {page.url}")
                
                try:
                    page.wait_for_selector("div.job-card", timeout=10000)
                    jobs = page.query_selector_all("div.job-card")
                except Exception as e:
                    logger.error(f"Không tìm thấy job cards: {e}")
                    break
                
                for job_card in jobs:
                    try:
                        job_card.click() # Chúng ta sẽ bỏ force=True và xử lý pop-up nếu có
                        page.wait_for_selector(".job-description-container", timeout=5000)

                        # Bước 1: Tìm các phần tử cha
                        header = page.query_selector(".sticky-container")
                        details_container = page.query_selector(".job-description-container")

                        # Bước 2: Tìm từng phần tử con và lấy text một cách an toàn
                        # TITLE
                        title_el = header.query_selector(".job-title.heading") if header else None
                        if title_el:
                            title = title_el.inner_text().strip()
                        else:
                            title = "N/A"
                            logger.warning("Không tìm thấy selector cho 'title'") # <-- Log để debug

                        # COMPANY
                        company_el = header.query_selector(".company") if header else None
                        if company_el:
                            company = company_el.inner_text().strip()
                        else:
                            company = "N/A"
                            logger.warning("Không tìm thấy selector cho 'company'") # <-- Log để debug

                        # TIME POSTED
                        time_el = header.query_selector(".listed-date") if header else None
                        if time_el:
                            time_posted = time_el.inner_text().strip()
                        else:
                            time_posted = "N/A"
                            logger.warning("Không tìm thấy selector cho 'time_posted'") # <-- Log để debug

                        # DESCRIPTION
                        if details_container:
                            description = details_container.inner_text().strip()
                        else:
                            description = "N/A"
                            logger.warning("Không tìm thấy selector cho 'description'") # <-- Log để debug
                        
                        # Bước 3: Ghi dữ liệu
                        job_data = {
                            "title": title,
                            "company": company,
                            "time_posted": time_posted,
                            "description": description,
                            "crawled_at": datetime.now().isoformat()
                        }
                        
                        scraped_data.append(job_data)
                        logger.info(f"✅ Đã crawl: {title} tại {company}")

                    except Exception as e:
                        # TỐI ƯU LOG LỖI: In ra cả URL đang bị lỗi để dễ kiểm tra lại bằng tay
                        current_url = page.url
                        logger.warning(f"❌ Lỗi khi xử lý một job card tại URL: {current_url}. Lỗi: {e}")
            
                next_button = page.query_selector("a.next-page-button")
                if next_button and next_button.get_attribute("href"):
                    next_url = base_url + next_button.get_attribute("href")
                    logger.info(f"➡️  Chuyển sang trang tiếp theo: {next_url}")
                    page.goto(next_url)
                    page_num += 1
                else:
                    logger.info("✅ Hết trang, kết thúc crawl.")
                    break
                
    except Exception as e:
        logger.error(f"Lỗi nghiêm trọng trong quá trình crawl: {e}", exc_info=True)
        raise
    finally:
        if browser: browser.close()

    if not scraped_data:
        logger.warning("Không crawl được dữ liệu nào.")
        return None

    logger.info(f"Ghi {len(scraped_data)} jobs vào file {output_file_path}")
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)
    return output_file_path

def load_raw_json_to_sql_callable(**kwargs):
    ti = kwargs['ti']
    input_file_path = ti.xcom_pull(task_ids='crawl_and_save_locally_task')
    if not input_file_path:
        logger.warning("Không có file để xử lý. Bỏ qua.")
        return

    db_user = os.environ.get("DB_USER", "postgres")
    db_pass = os.environ.get("DB_PASS", "123456")
    db_name = os.environ.get("DB_NAME", "job_db")
    db_host = os.environ.get("DB_HOST", "host.docker.internal")
    db_port = os.environ.get("DB_PORT", "5432")
    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url)
    
    with open(input_file_path, 'r', encoding='utf-8') as f:
        data_to_load = json.load(f)
    
    if not data_to_load:
        logger.info("File dữ liệu rỗng.")
        return

    unique_jobs = { (job.get('title'), job.get('company')): job for job in data_to_load if job.get('title') and job.get('company') }
    deduplicated_data = list(unique_jobs.values())

    if not deduplicated_data:
        logger.info("Không có dữ liệu hợp lệ sau khi khử trùng lặp.")
        return

    try:
        with engine.connect() as connection:
            logger.info("Kiểm tra và tạo bảng 'jobs' nếu cần...")
            METADATA.create_all(engine, checkfirst=True) # Chỉ tạo bảng 'jobs'
            
            insert_stmt = pg_insert(JOBS_TABLE).values(deduplicated_data)
            do_nothing_stmt = insert_stmt.on_conflict_do_nothing(
                index_elements=['title', 'company']
            )
            
            with connection.begin() as transaction:
                result = connection.execute(do_nothing_stmt)
                logger.info(f"✅ Đã chèn {result.rowcount} jobs thô mới vào database.")
                
    except Exception as e:
        logger.error(f"❌ Lỗi khi ghi dữ liệu thô vào database: {e}")
        raise