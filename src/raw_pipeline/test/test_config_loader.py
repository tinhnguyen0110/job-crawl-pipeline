import pytest
import yaml
import os
import tempfile
from config.config_loader import load_config


def test_load_config_success():
    """Test that config loads successfully"""
    config = load_config()
    
    # Check that config is a dictionary
    assert isinstance(config, dict)
    
    # Check required sections exist
    assert "project" in config
    assert "crawling" in config
    assert "output" in config
    assert "logging" in config
    assert "database" in config
    

def test_config_has_required_fields():
    """Test that config contains all required fields"""
    config = load_config()
    
    # Project section
    assert "name" in config["project"]
    assert "version" in config["project"]
    
    # Crawling section
    assert "source" in config["crawling"]
    assert "url" in config["crawling"]
    assert "csv_output_path" in config["crawling"]
    
    # Output section
    assert "save_to_csv" in config["output"]
    assert "structured_csv_path" in config["output"]
    
    # Database section
    assert "host" in config["database"]
    assert "port" in config["database"]
    assert "dbname" in config["database"]
    assert "user" in config["database"]


def test_config_values_are_correct_types():
    """Test that config values have correct data types"""
    config = load_config()
    
    # Project
    assert isinstance(config["project"]["name"], str)
    assert isinstance(config["project"]["version"], str)
    
    # Crawling
    assert isinstance(config["crawling"]["url"], str)
    assert isinstance(config["crawling"]["csv_output_path"], str)
    assert isinstance(config["crawling"]["timeout"], int)
    assert isinstance(config["crawling"]["max_retries"], int)
    assert isinstance(config["crawling"]["headless"], bool)
    
    # Output
    assert isinstance(config["output"]["save_to_csv"], bool)
    
    # Database
    assert isinstance(config["database"]["port"], int)


def test_config_file_missing():
    """Test behavior when config file is missing"""
    # This test assumes the config file path is hardcoded
    # In practice, we would want to make this configurable for testing
    pass  # For now, we'll skip this as it would require refactoring the config_loader


if __name__ == "__main__":
    pytest.main([__file__])