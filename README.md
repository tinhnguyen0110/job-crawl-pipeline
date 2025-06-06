<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<img src="readmeai/assets/logos/purple.svg" width="30%" style="position: relative; top: 0; right: 0;" alt="Project Logo"/>

# CRAWL2INSIGHT_2

<em>Vantage Point for AI Job Insights</em>

<!-- BADGES -->
<!-- local repository, no metadata badges. -->

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Redis-FF4438.svg?style=default&logo=Redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=default&logo=Docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=default&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/pandas-150458.svg?style=default&logo=pandas&logoColor=white" alt="pandas">
<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=default&logo=YAML&logoColor=white" alt="YAML">

</div>
<br>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
    - [Project Index](#project-index)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

Crawl2Insight_2 is an open-source data analysis toolkit that simplifies your web scraping, data processing, and AI-driven insights efforts! The core features include:

   - **📈🔢** Seamlessly set up a comprehensive Apache Airflow cluster with Docker Compose.
   - **🌐💻** Effortlessly fetch, process, and analyze diverse datasets using specified Python libraries.
   - **🚀🎯** Continuously develop a job crawl pipeline with GitHub integration and AI-powered analysis.
   - **📦🔧** Manage project dependencies easily thanks to well-organized `docker-compose.yaml`, `requirements.txt`, and Airflow-specific files.
   - **💻⚙️** Empower yourself with a user interface for conveniently browsing through job opportunities using Streamlit.
   - **🔥🔄** Simplify data ingestion, processing, and maintenance by automating the end-to-end pipeline process from crawling to analysis.

---

## Features

|      | Component       | Details                                                        |
| :--- | :-------------- | :------------------------------------------------------------- |
| ⚙️  | **Architecture**  | Multiple processes and services, utilizing Docker Compose for containerization. |
| 🔩 | **Code Quality**  | Moderate adherence to coding standards, with some areas needing improvement. Uses modern Python libraries such as `pandas`, `dateparser`, `requests`. |
| 📄 | **Documentation** | Documentation is provided for Docker setup and Airflow's Dockerfile. Additional documentation is recommended for project structure and usage. |
| 🔌 | **Integrations**  | Integrates with several CI/CD tools: `docker`, `pip`, `docker-compose.yaml`, `docker-compose.postgres.yaml`, Git (via `testgit.txt`), and Airflow-specific tools such as `flower`, `airflow-init`, `airflow-webserver`, `airflow-worker`. Also integrates with external APIs using `requests`. |
| 🧩 | **Modularity**    | Moderate modularity, with some shared functionality across scripts. Additional abstraction and encapsulation is recommended for better reusability. |
| 🧪 | **Testing**       | Uses testing libraries such as `unittest` (implied by the usage of functions with `test` prefix). However, test coverage needs to be improved.                   |
| ⚡️  | **Performance**   | Performance is reasonable for the current use case, but may require optimization for larger datasets or more complex tasks.    |
| 🛡️ | **Security**      | Limited security considerations are found, with no apparent implementation of secure coding practices or authentication mechanisms within the codebase. It's recommended to follow OWASP guidelines and implement necessary security measures. |
| 📦 | **Dependencies**  | Dependencies include Python libraries such as `pandas`, `dateparser`, `requests`, Airflow-specific libraries, and PostgreSQL for database storage. The complete list can be found in `requirements.txt` and `airflow/requirements.txt`. |
| 🚀 | **Scalability**   | Achieves some level of scalability through the use of Docker Compose to manage multiple containers. However, further improvements are needed for handling larger workloads or distributed processing. |

---

## Project Structure

```sh
└── Crawl2Insight_2/
    ├── airflow
    │   ├── dags
    │   ├── Dockerfile
    │   ├── logs
    │   └── requirements.txt
    ├── app
    │   └── job_browser.py
    ├── data
    │   ├── processed
    │   └── raw
    ├── db
    │   ├── __init__.py
    │   ├── __pycache__
    │   └── init_db.py
    ├── Docker
    │   ├── docker-compose.postgres.yaml
    │   └── scripts
    ├── docker-compose.yaml
    ├── logs
    │   └── pipeline.log
    ├── readme-ai.md
    ├── readme-ai_v1.md
    ├── README.md
    ├── requirements.txt
    ├── src
    │   ├── config
    │   ├── crawl
    │   ├── ingestion
    │   ├── pipeline
    │   ├── processing
    │   └── utils
    ├── test
    │   ├── __init__.py
    │   ├── __pycache__
    │   └── test_jobstreet_live.py
    └── testgit.txt
```

### Project Index

<details open>
	<summary><b><code>D:\DATA\CRAWL2INSIGHT_2/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/docker-compose.yaml'>docker-compose.yaml</a></b></td>
					<td style='padding: 8px;'>- Configures a comprehensive Airflow cluster using Docker Compose, leveraging CeleryExecutor with Redis and PostgreSQL<br>- This setup is intended for local development and includes support for environment variables or.env file configurations<br>- The docker-compose.yaml file defines services for Airflow webserver, scheduler, worker, triggerer, init, CLI, and an optional flower interface<br>- The architecture establishes connections between essential components such as Redis, PostgreSQL, and the custom Airflow image.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/requirements.txt'>requirements.txt</a></b></td>
					<td style='padding: 8px;'>- This project is an open-source data analysis toolkit<br>- The requirements.txt file specifies the dependencies needed for its operation, including requests, pandas, and dateparser libraries<br>- These tools empower users to fetch, process, and analyze diverse datasets with ease, making it an invaluable resource for data scientists and analysts alike.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/testgit.txt'>testgit.txt</a></b></td>
					<td style='padding: 8px;'>- Data\Crawl2Insight_2, utilizing a specified temperature level for results diversity<br>- The pipeline runs on a server located at qwen3:8b.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- airflow Submodule -->
	<details>
		<summary><b>airflow</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ airflow</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/airflow\Dockerfile'>Dockerfile</a></b></td>
					<td style='padding: 8px;'>- This Dockerfile builds an Apache Airflow container, version 2.8.1 with Python 3.10<br>- It installs specified Python packages and dependencies, including Playwright, to ensure seamless and efficient data pipeline orchestration in the Airflow environment.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/airflow\requirements.txt'>requirements.txt</a></b></td>
					<td style='padding: 8px;'>- Manages project dependencies using Airflow, a platform to programmatically schedule and monitor data pipelines<br>- The provided requirements file includes packages like Playwright, Requests, Pandas, Psycopg2, and Dateparser-essential tools for web scraping, HTTP interactions, data manipulation, database access, and date parsing, respectively-ensuring seamless data pipeline execution and flexibility in handling diverse data sources.</td>
				</tr>
			</table>
			<!-- dags Submodule -->
			<details>
				<summary><b>dags</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ airflow.dags</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/airflow\dags\crawl2insight_dag.py'>crawl2insight_dag.py</a></b></td>
							<td style='padding: 8px;'>- The <code>crawl2insight_dag.py</code> file is a scheduled Airflow task that initiates the run_pipeline daily, which in turn runs a custom Python script located at /opt/airflow/src/pipeline/run_pipeline.py<br>- This architecture automates the execution of the pipeline process aimed at data crawling and deriving insights from it.</td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- app Submodule -->
	<details>
		<summary><b>app</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ app</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/app\job_browser.py'>job_browser.py</a></b></td>
					<td style='padding: 8px;'>- The provided Python script, <code>app/job_browser.py</code>, serves as a user interface for exploring job listings within the larger project architecture<br>- It fetches job data from a database, filters and sorts jobs based on location and seniority level, and displays the results in an efficient manner using Streamlit<br>- This tool enables users to quickly browse through available job opportunities in their desired field and location.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- db Submodule -->
	<details>
		<summary><b>db</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ db</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/db\init_db.py'>init_db.py</a></b></td>
					<td style='padding: 8px;'>- Initializes a database to store and structure raw job data, including title, company, description, time posted, date crawled, job title, seniority, company location, salary, job requirements, benefits, date posted, and model details<br>- The structured table is created using machine learning models for further analysis.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- Docker Submodule -->
	<details>
		<summary><b>Docker</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ Docker</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/Docker\docker-compose.postgres.yaml'>docker-compose.postgres.yaml</a></b></td>
					<td style='padding: 8px;'>- The provided YAML file sets up a Docker Compose configuration for a PostgreSQL database server named job_pg<br>- It establishes an environment with the specified image, network port mapping, and basic credentials<br>- Additionally, it utilizes volume persistence to store data on the host machine, ensuring data continuity across container lifecycle restarts<br>- This configuration is essential for managing a PostgreSQL database within your job-related project architecture.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- src Submodule -->
	<details>
		<summary><b>src</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ src</b></code>
			<!-- config Submodule -->
			<details>
				<summary><b>config</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.config</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/src\config\config.yaml'>config.yaml</a></b></td>
							<td style='padding: 8px;'>- The <code>config.yaml</code> file provides configuration settings for the Crawl2Insight project, which automates job data collection from JobStreet using a user agent, set timeouts, and csv output paths<br>- It also initializes an Ollama model, specifies logging levels and locations, and configures database connections<br>- This setup enables the application to gather relevant AI jobs data for processing and analysis.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/src\config\config_loader.py'>config_loader.py</a></b></td>
							<td style='padding: 8px;'>- The <code>config_loader.py</code> module in the given project structure is responsible for loading configuration settings from a YAML file, located within the config directory<br>- This enables the application to access and utilize necessary configurations at runtime, promoting flexibility and ease of setup across diverse environments.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- crawl Submodule -->
			<details>
				<summary><b>crawl</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.crawl</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/src\crawl\jobstreet_crawler.py'>jobstreet_crawler.py</a></b></td>
							<td style='padding: 8px;'>- This Python script automates the crawling of JobStreet AI job listings in Vietnam, storing their details in a CSV file<br>- The code employs Playwright to interact with the JobStreet website and collect relevant information such as job title, company, description, time posted, and date crawled<br>- It dynamically navigates through multiple pages of the website for more comprehensive results and ensures output file existence before writing data.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- ingestion Submodule -->
			<details>
				<summary><b>ingestion</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.ingestion</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/src\ingestion\insert_raw_jobs.py'>insert_raw_jobs.py</a></b></td>
							<td style='padding: 8px;'>- This script imports job listings from a CSV file into a PostgreSQL database, specifically the raw_jobs table<br>- The data consists of job title, company, description, time posted, and date crawled<br>- Conflict resolution is handled by ignoring duplicates based on title, company, and date crawled<br>- This process enables real-time data ingestion and maintenance of a job listing dataset.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/src\ingestion\insert_structured_jobs.py'>insert_structured_jobs.py</a></b></td>
							<td style='padding: 8px;'>- This script is a Python tool that imports data from a CSV file and inserts it into a PostgreSQL database, updating existing records if necessary<br>- Its part of a larger job board application (src/ingestion) where structured job listings are processed to ensure theyre accurately represented within the system.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- pipeline Submodule -->
			<details>
				<summary><b>pipeline</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.pipeline</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/src\pipeline\run_pipeline.py'>run_pipeline.py</a></b></td>
							<td style='padding: 8px;'>- Crawling, data ingestion, raw data processing, structured data insertion into the database<br>- By executing this script, it triggers the entire cycle, providing structured job data for further analysis or use in other applications.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/src\pipeline\__main__.py'>__main__.py</a></b></td>
							<td style='padding: 8px;'>- The <code>src\pipeline\__main__.py</code> file serves as the entry point of this open-source data pipeline, triggering the execution of the defined operations or workflows when run directly<br>- The pipeline processes, transforms, and analyzes data from various sources as specified in the codebase hierarchy.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- processing Submodule -->
			<details>
				<summary><b>processing</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.processing</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/src\processing\process_raw_jobs.py'>process_raw_jobs.py</a></b></td>
							<td style='padding: 8px;'>- This Python script, placed within <code>src/processing/process_raw_jobs.py</code>, processes raw job data from a database and uses an external OLLAMA model to extract and structure relevant information (job title, seniority level, location, salary, job description, requirements, benefits, and post date) from job titles and descriptions<br>- These structured data are then saved in a CSV file for further analysis or use in other applications.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- utils Submodule -->
			<details>
				<summary><b>utils</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.utils</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/src\utils\logger.py'>logger.py</a></b></td>
							<td style='padding: 8px;'>- Enables structured logging across the application using a custom logger instance, defined by name and log level (INFO by default)<br>- Provides flexible configuration for formatting and outputting log messages to stdout, promoting consistent and error-free logging practices throughout the project.</td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- test Submodule -->
	<details>
		<summary><b>test</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ test</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='D:\Data\Crawl2Insight_2/blob/master/test\test_jobstreet_live.py'>test_jobstreet_live.py</a></b></td>
					<td style='padding: 8px;'>- This script initiates and tests the data extraction of AI job listings from JobStreet, a popular job board<br>- By utilizing the jobstreet_crawler module and configuring settings from a separate configuration file, it generates a CSV output containing job titles, descriptions, and other relevant details<br>- It ensures data integrity by removing any pre-existing CSV output before the crawl, verifying its creation after the process, and validating the resulting dataset for correct formatting and non-emptiness.</td>
				</tr>
			</table>
		</blockquote>
	</details>
</details>

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip
- **Container Runtime:** Docker

### Installation

Build Crawl2Insight_2 from the source and intsall dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone ../Crawl2Insight_2
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd Crawl2Insight_2
    ```

3. **Install the dependencies:**

<!-- SHIELDS BADGE CURRENTLY DISABLED -->
	<!-- [![docker][docker-shield]][docker-link] -->
	<!-- REFERENCE LINKS -->
	<!-- [docker-shield]: https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white -->
	<!-- [docker-link]: https://www.docker.com/ -->

	**Using [docker](https://www.docker.com/):**

	```sh
	❯ docker build -t Data/Crawl2Insight_2 .
	```
<!-- SHIELDS BADGE CURRENTLY DISABLED -->
	<!-- [![pip][pip-shield]][pip-link] -->
	<!-- REFERENCE LINKS -->
	<!-- [pip-shield]: https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white -->
	<!-- [pip-link]: https://pypi.org/project/pip/ -->

	**Using [pip](https://pypi.org/project/pip/):**

	```sh
	❯ pip install -r requirements.txt, airflow\requirements.txt
	```

### Usage

Run the project with:

**Using [docker](https://www.docker.com/):**
```sh
docker run -it {image_name}
```
**Using [pip](https://pypi.org/project/pip/):**
```sh
python {entrypoint}
```

### Testing

Crawl2insight_2 uses the {__test_framework__} test framework. Run the test suite with:

**Using [pip](https://pypi.org/project/pip/):**
```sh
pytest
```

---

## Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

## Contributing

- **💬 [Join the Discussions](https://LOCAL/Data/Crawl2Insight_2/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://LOCAL/Data/Crawl2Insight_2/issues)**: Submit bugs found or log feature requests for the `Crawl2Insight_2` project.
- **💡 [Submit Pull Requests](https://LOCAL/Data/Crawl2Insight_2/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your LOCAL account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone D:\Data\Crawl2Insight_2
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to LOCAL**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://LOCAL{/Data/Crawl2Insight_2/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Data/Crawl2Insight_2">
   </a>
</p>
</details>

---

## License

Crawl2insight_2 is protected under the [LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## Acknowledgments

- Credit `contributors`, `inspiration`, `references`, etc.

<div align="right">

[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
