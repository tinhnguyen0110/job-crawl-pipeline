import pandas as pd
import psycopg2
from psycopg2 import sql
from config.config_loader import load_config

from utils.logger import get_logger

logger = get_logger(__name__)

def insert_structured_to_db():
    config = load_config()
    db_config = config['database']
    csv_file = config['output']['structured_csv_path']

    if not csv_file or not csv_file.endswith(".csv"):
        logger.error(f"❌ Đường dẫn file CSV không hợp lệ: {csv_file}")
        return

    try:
        df = pd.read_csv(csv_file)
        logger.info(f"📥 Đọc file CSV: {csv_file} - {len(df)} dòng")

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        logger.info("🔌 Kết nối database thành công.")

        insert_query = sql.SQL("""
            INSERT INTO structured_jobs (
                id, job_title, seniority, company, location, salary,
                job_description, job_requirements, benefits, date_posted, model
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
            job_title = EXCLUDED.job_title,
            seniority = EXCLUDED.seniority,
            company = EXCLUDED.company,
            location = EXCLUDED.location,
            salary = EXCLUDED.salary,
            job_description = EXCLUDED.job_description,
            job_requirements = EXCLUDED.job_requirements,
            benefits = EXCLUDED.benefits,
            date_posted = EXCLUDED.date_posted,
            model = EXCLUDED.model;
        """)

        for idx, row in df.iterrows():
            values = (
                int(row['id']),
                row.get('job_title', ''),
                row.get('seniority', ''),
                row.get('company', ''),
                row.get('location', ''),
                row.get('salary', ''),
                row.get('job_description', ''),
                row.get('job_requirements', ''),
                row.get('benefits', ''),
                row.get('post_date', None),
                row.get('model', '')
            )
            try:
                cursor.execute(insert_query, values)
                logger.debug(f"✅ Insert/Update job ID: {row['id']}")
            except Exception as inner_e:
                logger.warning(f"⚠️ Lỗi khi xử lý ID {row['id']}: {inner_e}")
                conn.rollback()

        conn.commit()
        logger.info("📦 Đã commit toàn bộ dữ liệu.")
        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"❌ Lỗi khi insert dữ liệu: {e}")

if __name__ == "__main__":
    insert_structured_to_db()
