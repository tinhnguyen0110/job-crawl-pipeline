# Test Suite for Raw Pipeline

This directory contains the test suite for the raw job crawling pipeline.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:
   ```bash
   # Run only unit tests (recommended for CI)
   python run_tests.py unit

   # Run integration tests (requires internet connection)
   python run_tests.py integration

   # Run all tests
   python run_tests.py all
   ```

## Test Types

### Unit Tests
- Fast, isolated tests that don't require external resources
- Test individual functions and classes
- Marked with `@pytest.mark.unit` (optional)

### Integration Tests
- Tests that require external resources (internet, file system, etc.)
- Marked with `@pytest.mark.integration`
- May be slower and can fail due to external factors

## Test Structure

```
test/
├── __init__.py
├── test_config_loader.py      # Tests for configuration loading
├── test_logger.py             # Tests for logging utilities
└── test_jobstreet_live.py     # Tests for JobStreet crawler (includes integration test)
```

## Coverage

Test coverage reports are generated in `htmlcov/` directory. Open `htmlcov/index.html` in a browser to view detailed coverage.

## CI/CD Integration

For CI/CD pipelines, use:
```bash
python run_tests.py unit
```

This excludes integration tests that may fail in CI environments due to network restrictions or external service availability.