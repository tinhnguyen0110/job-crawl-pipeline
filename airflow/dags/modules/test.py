# dags/modules/crawling.py

import os

import json

import logging

from datetime import datetime

from playwright.sync_api import sync_playwright



# Thiết lập một logger riêng cho module này

logger = logging.getLogger(__name__)



def crawl_jobstreet_to_local_callable(**kwargs):

    """

    Hàm Python này được thiết kế để Airflow gọi thông qua PythonOperator.

   

    Nó thực hiện các công việc sau:

    1. Lấy các tham số (URL, thư mục output) từ context của Airflow.

    2. Sử dụng Playwright để crawl dữ liệu từ JobStreet.

    3. Thu thập dữ liệu vào một danh sách (list).

    4. Ghi toàn bộ danh sách vào một file JSON duy nhất trên local filesystem của worker.

    5. Trả về đường dẫn của file đã tạo để các task sau có thể sử dụng qua XComs.

    """

    # Lấy các tham số và context từ Airflow

    params = kwargs.get("params", {})

    logical_date = kwargs["ds"] # Ví dụ: '2025-06-12'

    run_id = kwargs["run_id"]   # Ví dụ: 'scheduled__2025-06-12T00:00:00+00:00'

   

    start_url = params.get("start_url")

    if not start_url:

        raise ValueError("Không tìm thấy 'start_url' trong params của DAG.")



    # ===================================================================

    # ==            ✅ THAY ĐỔI DUY NHẤT ĐƯỢC ÁP DỤNG Ở ĐÂY           ==

    # ===================================================================

    # Tối ưu hóa việc đặt tên file để nó duy nhất cho mỗi lần chạy DAG,

    # tránh xung đột khi chạy lại (retry) hoặc chạy song song.



    # Tạo một tên file an toàn từ run_id (thay thế các ký tự không hợp lệ)

    safe_run_id = run_id.replace(":", "_").replace("+", "_")

   

    # Tạo thư mục con dựa trên ngày chạy để dễ quản lý file

    output_dir = f"/opt/airflow/data/{logical_date}"

    output_filename = f"{safe_run_id}.json" # Tên file giờ là run_id đã được làm sạch

    output_file_path = os.path.join(output_dir, output_filename)

    # ===================================================================



    logger.info(f"🚀 Bắt đầu crawl từ URL: {start_url}")

    logger.info(f"📁 File output sẽ được lưu tại: {output_file_path}")



    # Đảm bảo thư mục output tồn tại

    os.makedirs(output_dir, exist_ok=True)



    scraped_data = [] # Nơi lưu trữ tạm thời dữ liệu crawl được



    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto(start_url)

           

            base_url = "https://www.jobstreet.vn"

            page_num = 1

            # Giới hạn crawl 2 trang để test nhanh, bạn có thể bỏ giới hạn này

            while page_num <= 2:

                logger.info(f"🔄 Đang xử lý trang {page_num}...")

                try:

                    logger.info("Đang tìm kiếm job cards trên trang...")

                    page.wait_for_selector("div.job-card", timeout=3000)

                    jobs_on_page = page.query_selector_all("div.job-card")

                except Exception as e:

                    logger.error(e)

                    logger.error(f"❌ Không tìm thấy job cards trên trang {page.url}")

                    break



                for job_card in jobs_on_page:

                    try:

                        job_card.click(force=True)

                        page.wait_for_selector(".job-description-container", timeout=5000)



                        header = page.query_selector(".sticky-container")

                        title = header.query_selector(".job-title.heading").inner_text().strip() if header else "N/A"

                        company = header.query_selector(".company").inner_text().strip() if header else "N/A"

                        time_posted = header.query_selector(".listed-date").inner_text().strip() if header else "N/A"

                        description = page.query_selector(".job-description-container").inner_text().strip()



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

                        logger.warning(f"❌ Lỗi khi xử lý một job card: {e}")



                # Điều hướng sang trang tiếp theo

                next_button = page.query_selector("a.next-page-button")

                if next_button and next_button.get_attribute("href"):

                    next_url = base_url + next_button.get_attribute("href")

                    logger.info(f"➡️  Chuyển sang trang tiếp theo: {next_url}")

                    page.goto(next_url)

                    page_num += 1

                else:

                    logger.info("✅ Hết trang, kết thúc crawl.")

                    break

           

            browser.close()



    except Exception as e:

        logger.error(f"Lỗi nghiêm trọng trong quá trình crawl: {e}")

        # Ném lỗi ra ngoài để Airflow biết task này đã thất bại

        raise



    if not scraped_data:

        logger.warning("Không crawl được dữ liệu nào.")

        return None



    # Ghi dữ liệu vào file JSON

    logger.info(f"Ghi {len(scraped_data)} jobs vào file {output_file_path}")

    with open(output_file_path, "w", encoding="utf-8") as f:

        json.dump(scraped_data, f, indent=2, ensure_ascii=False)



    # Trả về đường dẫn file, Airflow sẽ tự động lưu vào XComs

    return output_file_path