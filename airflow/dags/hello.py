from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

with DAG(
    dag_id="hello_world_2",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,          # Không chạy backlog -> không cần tạo run cũ
    tags=["demo"],
) as dag:
    DummyOperator(task_id="start")