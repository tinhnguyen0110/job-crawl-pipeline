# run_pipeline.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crawl.jobstreet_crawler import crawl_jobstreet_ai_jobs
from ingestion.insert_raw_jobs import import_csv_to_db
from processing.process_raw_jobs import process_raw_jobs
from ingestion.insert_structured_jobs import insert_structured_to_db
from config.config_loader import load_config
from utils.logger import get_logger  # logger chuẩn dùng chung

logger = get_logger("pipeline")

def main():
    try:
        config = load_config()
        csv_raw_path = config["crawling"]["csv_output_path"]
        csv_structured_path = config["output"]["structured_csv_path"]

        crawl_jobstreet_ai_jobs()
        import_csv_to_db()
        process_raw_jobs()
        insert_structured_to_db()

        logger.info("🎉 Pipeline hoàn tất thành công.")

    except Exception as e:
        logger.exception("❌ Pipeline lỗi: %s", e)

if __name__ == "__main__":
    main()