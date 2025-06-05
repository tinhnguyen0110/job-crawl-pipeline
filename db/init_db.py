from config.config_loader import load_config
import psycopg2

CREATE_RAW_JOBS_TABLE = """
CREATE TABLE IF NOT EXISTS raw_jobs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    company TEXT,
    description TEXT,
    time_posted TEXT,
    date_crawled DATE
);
"""

CREATE_STRUCTURED_JOBS_TABLE = """
CREATE TABLE IF NOT EXISTS structured_jobs (
    id INTEGER PRIMARY KEY,
    job_title TEXT,
    seniority TEXT,
    company TEXT,
    location TEXT,
    salary TEXT,
    job_description TEXT,
    job_requirements TEXT,
    benefits TEXT,
    date_posted DATE,
    model TEXT
);
"""

def init_db():
    config = load_config()
    db_config = config['database']

    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(CREATE_RAW_JOBS_TABLE)
        cursor.execute(CREATE_STRUCTURED_JOBS_TABLE)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")

if __name__ == "__main__":
    init_db()
