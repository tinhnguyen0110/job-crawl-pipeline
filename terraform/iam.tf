

#========= cấp quyền cho cụm ứng dụng ===========
resource "google_service_account" "gke_node_sa" {
  project      = var.project_id
  account_id   = "gke-node-sa"
  display_name = "Service Account for Crawl2Insight GKE Nodes"
}

# Cấp quyền ghi log cho Service Account
resource "google_project_iam_member" "gke_sa_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.gke_node_sa.email}"
}

# Cấp quyền gửi metrics giám sát
resource "google_project_iam_member" "gke_sa_monitoring" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.gke_node_sa.email}"
}

# Cấp quyền đọc/kéo image từ Registry
resource "google_project_iam_member" "gke_sa_artifact_registry" {
  project = var.project_id
  role    = "roles/artifactregistry.reader" # <-- Vai trò chính xác
  member  = "serviceAccount:${google_service_account.gke_node_sa.email}"
}

#========= cấp quyền cho Application ===========
resource "google_service_account" "fastapi_app_sa" {
  project      = var.project_id
  account_id   = "fastapi-app-sa-crawl2insight"
  display_name = "Service Account for FastAPI Backend Application"
}

# Cấp quyền Cloud SQL Client cho GSA của ứng dụng
resource "google_project_iam_member" "fastapi_sa_cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.fastapi_app_sa.email}"
}

# Liên kết GSA của app với KSA trong cluster
resource "google_service_account_iam_member" "fastapi_workload_binding" {
  service_account_id = google_service_account.fastapi_app_sa.name
  role               = "roles/iam.workloadIdentityUser"
  # Định danh của KSA, theo định dạng chuẩn của Workload Identity
  # Cú pháp: serviceAccount:PROJECT_ID.svc.id.goog[K8S_NAMESPACE/KSA_NAME]
  member             = "serviceAccount:${var.project_id}.svc.id.goog[application/fastapi-backend-ksa]"
}

#========= cấp quyền cho Airflow ===========
# Service Account dành riêng cho ứng dụng Airflow
resource "google_service_account" "airflow_sa" {
  project      = var.project_id
  account_id   = "airflow-sa-crawl2insight"
  display_name = "Service Account for Airflow"
}


# Cấp quyền Cloud SQL Client cho GSA của ứng dụng
resource "google_project_iam_member" "airflow_sa_cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.airflow_sa.email}"
}

resource "google_project_iam_member" "airflow_sa_storage_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.airflow_sa.email}"
}

resource "google_storage_bucket_iam_member" "airflow_log_access" {
  bucket = "airflow-logs-tinhnv-gke"
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.airflow_sa.email}"
}


# Liên kết GSA của app với KSA trong cluster
resource "google_service_account_iam_member" "airflow_workload_binding" {
  service_account_id = google_service_account.airflow_sa.name
  role               = "roles/iam.workloadIdentityUser"
  # Định danh của KSA, theo định dạng chuẩn của Workload Identity
  # Cú pháp: serviceAccount:PROJECT_ID.svc.id.goog[K8S_NAMESPACE/KSA_NAME]
  member             = "serviceAccount:${var.project_id}.svc.id.goog[airflow/airflow-ksa]"
}