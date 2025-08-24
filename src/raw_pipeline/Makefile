# Makefile for raw pipeline testing and development

.PHONY: test test-unit test-integration test-all clean install

# Install dependencies
install:
	pip install -r requirements.txt

# Run unit tests only (fast, no external dependencies)
test-unit:
	python run_tests.py unit

# Run integration tests only (may require internet/external resources)
test-integration:
	python run_tests.py integration

# Run all tests
test-all:
	python run_tests.py all

# Default test target (unit tests for CI)
test: test-unit

# Clean test artifacts
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete