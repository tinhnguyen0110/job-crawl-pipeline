# include/modules/io_utils.py
import os
import json
import logging
# Không cần import Variable nữa
# from airflow.models import Variable 
from google.cloud import storage
from google.api_core.exceptions import GoogleAPICallError

logger = logging.getLogger(__name__)

# TODO: Sau này, hãy chuyển cấu hình này sang Airflow Variables cho production.
SAVE_CONFIG = {
    # Thay đổi giá trị này thành "GCS" để lưu lên cloud.
    "destination": "GCS", 
    
    # Điền sẵn tên GCS bucket của bạn
    "gcs_bucket": "airflow-logs-tinhnv-gke" 
}
# ===================================================================


def save_data_to_destination(data_to_save: list, logical_date: str, run_id: str) -> str:
    # Lấy cấu hình từ dictionary đã định nghĩa ở trên
    destination = SAVE_CONFIG.get("destination", "LOCAL").upper()
    
    safe_run_id = run_id.replace(":", "_").replace("+", "_")
    output_filename = f"{safe_run_id}.json"

    if destination == "GCS":
        try:
            bucket_name = SAVE_CONFIG.get("gcs_bucket")
            if not bucket_name:
                raise ValueError("Tên GCS bucket chưa được cấu hình trong SAVE_CONFIG.")
                
            blob_name = f"raw_data/{logical_date}/{output_filename}"
            
            logger.info(f"Đang upload dữ liệu lên GCS: gs://{bucket_name}/{blob_name}")
            
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            blob.upload_from_string(
                data=json.dumps(data_to_save, indent=2, ensure_ascii=False),
                content_type="application/json",
            )
            
            output_path = f"gs://{bucket_name}/{blob_name}"
            logger.info(f"✅ Upload thành công lên: {output_path}")
            return output_path
        except (GoogleAPICallError, Exception) as e:
            logger.error(f"❌ Lỗi khi upload lên GCS: {e}")
            raise

    # Mặc định hoặc nếu destination == "LOCAL"
    else:
        output_dir = f"/opt/airflow/data/{logical_date}"
        output_path = os.path.join(output_dir, output_filename)
        
        logger.info(f"Đang lưu dữ liệu vào file local: {output_path}")
        os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Lưu file local thành công.")
        return output_path