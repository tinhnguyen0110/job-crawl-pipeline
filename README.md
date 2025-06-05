# CRAWL2INSIGHT

CRAWL2INSIGHT is a data pipeline project for crawling, processing, and analyzing AI job postings from JobStreet.vn, using Apache Airflow, Docker, PostgreSQL, and Playwright.

## Features

- **Crawl AI job data** from JobStreet.vn using Playwright.
- **Clean and normalize data** before storage.
- **Automate the pipeline** with Apache Airflow.
- **Store data** in PostgreSQL.
- **Quick deployment** with Docker Compose.

## Architecture

- **Airflow:** Orchestrates the pipeline.
- **PostgreSQL:** Stores job data.
- **Redis:** Message broker for Celery.
- **Playwright:** Web crawling.
- **Docker Compose:** Manages all services.