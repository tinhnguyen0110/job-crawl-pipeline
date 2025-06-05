from playwright.sync_api import sync_playwright
from config.config_loader import load_config
import csv
import os
from datetime import datetime
from utils.logger import get_logger

logger = get_logger("crawler.jobstreet")
logger.info("🚀 Bắt đầu crawl JobStreet AI Jobs")

def crawl_jobstreet_ai_jobs():
    config = load_config()
    base_url = "https://www.jobstreet.vn"
    start_url = config["crawling"]["url"]
    csv_file = config["crawling"]["csv_output_path"]
    file_exists = os.path.isfile(csv_file)

    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "description", "time_posted", "date_crawled"])
        if not file_exists:
            writer.writeheader()

        with sync_playwright() as p:
            # browser = p.chromium.launch(
            #     headless=config["crawling"].get("headless", False),
            #     slow_mo=config["crawling"].get("slow_mo", 100)
            # )
            browser = p.chromium.launch(
                headless=True,
            )
            page = browser.new_page()
            page.goto(start_url)
            logger.info(f"Đang truy cập trang: {start_url}")

            page_num = 1
            while True:
                logger.info(f"\n🔄 Trang {page_num}...\n")
                
                try:
                    page.wait_for_selector("div.job-card", timeout=10000)
                    jobs = page.query_selector_all("div.job-card")
                except Exception as e:
                    logger.error(f"Không tìm thấy job cards: {e}")
                    break
                
                for idx, job in enumerate(jobs):
                    try:
                        job.click()
                        page.wait_for_selector(".job-description-container", timeout=10000)

                        header = page.query_selector(".sticky-container")
                        title_el = header.query_selector(".job-title.heading") if header else None
                        company_el = header.query_selector(".company") if header else None
                        time_el = header.query_selector(".listed-date") if header else None
                        details_el = page.query_selector(".job-description-container")

                        title = title_el.inner_text().strip() if title_el else "Không rõ"
                        company = company_el.inner_text().strip() if company_el else "Không rõ"
                        time_posted = time_el.inner_text().strip() if time_el else "Không rõ"
                        description = details_el.inner_text().strip() if details_el else "Không rõ"

                        writer.writerow({
                            "title": title,
                            "company": company,
                            "description": description,
                            "time_posted": time_posted,
                            "date_crawled": datetime.now().date().isoformat()
                        })

                        logger.debug(f"✅ [{idx+1}] {title} - {company}")
                        page.wait_for_timeout(300)

                    except Exception as e:
                        logger.warning(f"❌ Lỗi job {idx+1}: {e}")

                next_button = page.query_selector("a.next-page-button")
                if next_button:
                    next_href = next_button.get_attribute("href")
                    if not next_href:
                        logger.warning("⚠️ Không tìm thấy href của trang kế tiếp.")
                        break
                    next_url = base_url + next_href
                    logger.info(f"➡️ Chuyển sang: {next_url}")
                    page.goto(next_url)
                    try:
                        page.wait_for_selector(".dismiss", timeout=3000)
                        page.click(".dismiss")
                    except:
                        pass
                    page.wait_for_load_state("load")
                    page_num += 1
                    if page_num == 3:   
                        logger.info("⚠️ Dừng lại sau 2 trang để tránh quá tải.")
                        break
                else:
                    logger.info("\n✅ Hết trang.")
                    break

            browser.close()
    logger.info(f"\n📁 Đã lưu dữ liệu vào {csv_file}")

if __name__ == "__main__":
    crawl_jobstreet_ai_jobs()