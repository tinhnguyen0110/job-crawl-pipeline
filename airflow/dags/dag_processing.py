# dags/dag_processing.py

from __future__ import annotations
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Import hàm callable chính từ module processing
from modules.processing import process_jobs_and_update_db_callable

with DAG(
    dag_id="processing_llm_jobs",
    schedule_interval="0 */3 * * *", # Chạy mỗi giờ một lần để xử lý
    start_date=pendulum.datetime(2025, 6, 12, tz="Asia/Ho_Chi_Minh"),
    catchup=False,
    is_paused_upon_creation=False,
    max_active_runs=1, # Đảm bảo chỉ có 1 lần chạy xử lý tại một thời điểm
    params={
        "time_get_api": 0,
    },
    tags=['processing', 'llm']
) as dag:

    # Task 1: Task xử lý chính
    # Task này sẽ kết nối DB, lấy dữ liệu, gọi LLM và cập nhật lại DB.
    # Bên trong hàm đã có logic kiểm tra nếu không có dữ liệu mới thì sẽ kết thúc sớm.
    process_task = PythonOperator(
        task_id="process_jobs_and_update_db_task",
        python_callable=process_jobs_and_update_db_callable,
    )

    # Task 2: Task thông báo kết quả
    # Task này sẽ chạy sau khi task xử lý chính hoàn thành.
    send_notification_task = BashOperator(
        task_id="send_notification_task",
        # Không cần trigger_rule nữa vì đây là một chuỗi tuần tự đơn giản.
        # Airflow sẽ mặc định chạy task này chỉ khi task trước nó thành công.
        bash_command="""
        # Lấy kết quả trả về từ task trước qua XCom.
        # Nếu không có kết quả (ví dụ: không có job mới), sẽ dùng giá trị mặc định.
        PROCESS_RESULT="{{ ti.xcom_pull(task_ids='process_jobs_and_update_db_task') | default('Không có dữ liệu mới để xử lý.') }}"
        
        echo "Gửi thông báo - Pipeline xử lý LLM hoàn tất."
        echo "Kết quả: $PROCESS_RESULT"
        """,
    )

    # Định nghĩa luồng chạy tuần tự 2 bước
    process_task >> send_notification_task