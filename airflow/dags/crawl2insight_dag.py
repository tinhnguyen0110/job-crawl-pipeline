# airflow/dags/crawl2insight_dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {"start_date": datetime(2024, 1, 1)}

with DAG("crawl2insight_dag", schedule_interval="@daily", catchup=False, default_args=default_args) as dag:
    run_pipeline = BashOperator(
        task_id="run_pipeline",
        bash_command="python /opt/airflow/src/pipeline/run_pipeline.py"
    )
