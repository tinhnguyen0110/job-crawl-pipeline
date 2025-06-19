
#========= cấp quyền cho git ===========
# Quyền đẩy image lên Artifact Registry
resource "google_project_iam_member" "runner_artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.github_runner_sa.email}"
}

# Quyền deploy lên GKE
resource "google_project_iam_member" "runner_gke_developer" {
  project = var.project_id
  role    = "roles/container.developer"
  member  = "serviceAccount:${google_service_account.github_runner_sa.email}"
}

resource "google_service_account" "gitsync_ssh_key" {
  project      = var.project_id
  account_id   = "gitsync-ssh-key"
  display_name = "Service Account for GitSync SSH Key"
}

# Cấp quyền truy cập cho Service Account
resource "google_project_iam_member" "gitsync_ssh_key_access" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.gitsync_ssh_key.email}"
}

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

# Quyền đọc secret cho Airflow
resource "google_secret_manager_secret_iam_member" "airflow_fernet_key_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.airflow_fernet_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.airflow_sa.email}"
}


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

#========= cấp quyền cho litellm ===========

# Service Account dành riêng cho ứng dụng LiteLLM
resource "google_service_account" "litellm_sa" {
  project      = var.project_id
  account_id   = "litellm-sa-crawl2insight"
  display_name = "Service Account for LiteLLM"
}

# Quyền đọc secret cho LiteLLM
resource "google_secret_manager_secret_iam_member" "litellm_api_key_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.litellm_openai_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.litellm_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "litellm_ui_credentials_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.litellm_ui_credentials.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.litellm_sa.email}"
}

# Liên kết GSA của app với KSA trong cluster
resource "google_service_account_iam_member" "litellm_workload_binding" {
  service_account_id = google_service_account.litellm_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[platform-services/litellm-ksa]"
}