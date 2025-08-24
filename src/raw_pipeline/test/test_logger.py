import pytest
import logging
from utils.logger import get_logger


def test_get_logger_returns_logger():
    """Test that get_logger returns a logger instance"""
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)


def test_get_logger_with_name():
    """Test that logger has the correct name"""
    logger_name = "test_crawler"
    logger = get_logger(logger_name)
    assert logger.name == logger_name


def test_get_logger_default_level():
    """Test that logger has default INFO level"""
    logger = get_logger("test_logger")
    assert logger.level == logging.INFO


def test_get_logger_custom_level():
    """Test that logger accepts custom log level"""
    logger = get_logger("test_logger", "DEBUG")
    assert logger.level == logging.DEBUG
    
    logger = get_logger("test_logger", "ERROR")
    assert logger.level == logging.ERROR


def test_get_logger_invalid_level():
    """Test that logger handles invalid log level gracefully"""
    logger = get_logger("test_logger", "INVALID_LEVEL")
    # Should default to INFO for invalid levels
    assert logger.level == logging.INFO


def test_get_logger_has_handler():
    """Test that logger has a stream handler"""
    logger = get_logger("test_logger")
    assert len(logger.handlers) > 0
    
    # Check that it's a StreamHandler
    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)


def test_get_logger_no_duplicate_handlers():
    """Test that calling get_logger multiple times doesn't add duplicate handlers"""
    logger1 = get_logger("same_name")
    handler_count_1 = len(logger1.handlers)
    
    logger2 = get_logger("same_name")
    handler_count_2 = len(logger2.handlers)
    
    # Should be the same logger instance with same number of handlers
    assert logger1 is logger2
    assert handler_count_1 == handler_count_2


def test_logger_formatter():
    """Test that logger has correct formatter"""
    logger = get_logger("test_logger")
    handler = logger.handlers[0]
    formatter = handler.formatter
    
    # Check that formatter exists and has correct format
    assert formatter is not None
    assert "%(asctime)s" in formatter._fmt
    assert "%(name)s" in formatter._fmt
    assert "%(levelname)s" in formatter._fmt
    assert "%(message)s" in formatter._fmt


if __name__ == "__main__":
    pytest.main([__file__])