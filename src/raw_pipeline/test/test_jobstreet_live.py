import os
import csv
from crawl.jobstreet_crawler import crawl_jobstreet_ai_jobs
from config.config_loader import load_config

def test_crawl_jobstreet_live():
    config = load_config()
    csv_path = config["crawling"]["csv_output_path"]

    # Xóa file cũ nếu có
    if os.path.exists(csv_path):
        os.remove(csv_path)

    crawl_jobstreet_ai_jobs()

    # Kiểm tra file được tạo và có dữ liệu
    assert os.path.exists(csv_path)

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) > 0  # Có ít nhất 1 job
        assert "title" in rows[0]
        assert "description" in rows[0]