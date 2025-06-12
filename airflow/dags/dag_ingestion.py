from __future__ import annotations
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator # <-- Bỏ comment dòng này

# Import cả hai hàm từ các module tương ứng
from modules.crawling import crawl_jobstreet_to_local_callable,load_raw_json_to_sql_callable

with DAG(
    dag_id="etl_jobstreet_to_sql", # Đổi tên DAG cho rõ nghĩa hơn
    start_date=pendulum.datetime(2025, 6, 11, tz="Asia/Ho_Chi_Minh"),
    schedule_interval="@daily",
    catchup=False,
    params={
        "start_url": "https://www.jobstreet.vn/vi%E1%BB%87c-l%C3%A0m-Ai-Engineer",
    },
    tags=["etl", "crawling", "database"],
) as dag:
    
    crawl_task = PythonOperator(
        task_id="crawl_and_save_locally_task",
        python_callable=crawl_jobstreet_to_local_callable,
    )
    
    load_to_sql_task = PythonOperator(
        task_id="load_data_to_sql_task",
        python_callable=load_raw_json_to_sql_callable,
    )

    send_notification_task = BashOperator(
        task_id="send_notification_task", # Sửa lại tên task_id cho nhất quán
        bash_command="""
        # Lấy giá trị trả về từ task trước. Nếu không có giá trị (None), mặc định là 0.
        ROWS_INSERTED="{{ ti.xcom_pull(task_ids='load_data_to_sql_task') | default(0) }}"
        echo "Gửi thông báo: Pipeline hoàn tất. Đã chèn/cập nhật $ROWS_INSERTED bản ghi mới."
        """,
    )

    # Định nghĩa luồng chạy 3 bước
    crawl_task >> load_to_sql_task >> send_notification_task