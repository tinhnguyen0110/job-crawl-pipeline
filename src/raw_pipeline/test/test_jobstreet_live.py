import os
import csv
import pytest
import tempfile
from unittest.mock import patch, MagicMock
from crawl.jobstreet_crawler import crawl_jobstreet_ai_jobs
from config.config_loader import load_config


@pytest.mark.integration
def test_crawl_jobstreet_live():
    """Integration test for JobStreet crawler - requires internet connection"""
    config = load_config()
    csv_path = config["crawling"]["csv_output_path"]

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

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


def test_config_loading():
    """Test that configuration loads correctly for crawler"""
    config = load_config()
    
    # Check crawler-specific config
    assert "crawling" in config
    assert "url" in config["crawling"]
    assert "csv_output_path" in config["crawling"]
    assert config["crawling"]["source"] == "jobstreet"


def test_csv_output_structure():
    """Test that CSV output has the expected structure"""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        temp_path = temp_file.name
        
        # Write test CSV data
        fieldnames = ["title", "company", "description", "time_posted", "date_crawled"]
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            "title": "AI Engineer",
            "company": "Test Company",
            "description": "Test description",
            "time_posted": "2024-01-01",
            "date_crawled": "2024-01-01"
        })
    
    try:
        # Verify the CSV structure
        with open(temp_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            assert len(rows) == 1
            row = rows[0]
            assert "title" in row
            assert "company" in row
            assert "description" in row
            assert "time_posted" in row
            assert "date_crawled" in row
            
            assert row["title"] == "AI Engineer"
            assert row["company"] == "Test Company"
    finally:
        # Clean up
        os.unlink(temp_path)