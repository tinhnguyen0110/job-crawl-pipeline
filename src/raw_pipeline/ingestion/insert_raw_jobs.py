import logging
from config.config_loader import load_config
import psycopg2
import csv
import os

from utils.logger import get_logger

logger = get_logger(__name__)

INSERT_QUERY = """
INSERT INTO raw_jobs (title, company, description, time_posted, date_crawled)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (title, company, date_crawled) DO NOTHING;
"""

def import_csv_to_db():
    logger.info("🚀 Bắt đầu import dữ liệu từ CSV vào PostgreSQL")
    config = load_config()
    db_config = config["database"]
    csv_file_path = config["crawling"]["csv_output_path"]

    if not os.path.exists(csv_file_path):
        logger.warning(f"⚠️ File CSV không tồn tại: {csv_file_path}")
        return

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        logger.info("✅ Đã kết nối cơ sở dữ liệu thành công")

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                values = (
                    row['title'],
                    row['company'],
                    row['description'],
                    row['time_posted'],
                    row['date_crawled']
                )
                try:
                    cursor.execute(INSERT_QUERY, values)
                    conn.commit()
                    logger.debug(f"📥 Inserted: {row['title']} - {row['company']}")
                except Exception as e:
                    conn.rollback()
                    logger.error(f"❌ Lỗi khi insert: {e}")

        cursor.close()
        conn.close()
        logger.info("✅ Đã hoàn thành import dữ liệu")

    except Exception as e:
        logger.exception(f"❌ Không thể kết nối cơ sở dữ liệu: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import_csv_to_db()
