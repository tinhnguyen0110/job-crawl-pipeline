
#========= cấp quyền cho git ===========

resource "google_service_account" "github_runner_sa" {
  project      = var.project_id
  account_id   = "github-runner-sa"
  display_name = "Service Account for GitHub Actions Runner"
}

# Quyền đẩy image lên Artifact Registry
resource "google_project_iam_member" "runner_artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.github_runner_sa.email}"
}

# 1. Tạo một Workload Identity Pool
resource "google_iam_workload_identity_pool" "github_pool" {
  project                   = var.project_id
  workload_identity_pool_id = "github-actions-pool-v2"
  display_name              = "GitHub Actions Pool"
}

# 2. Tạo một Provider bên trong Pool đó cho GitHub
resource "google_iam_workload_identity_pool_provider" "github_provider" {
  project                            = var.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Actions Provider"
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    # Ánh xạ các thuộc tính từ GitHub token sang Google token
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }
  # Cho phép bất kỳ repo nào trong tổ chức/user của bạn
  # Để an toàn hơn, bạn có thể chỉ định repo cụ thể: "repo:your-github-org/your-repo-name"
  #attribute_condition = "assertion.repository.startsWith('repo:your-github-org/')"
  attribute_condition = "assertion.repository == 'tinhnguyen0110/job-crawl-pipeline'"
}

# 3. Cấp quyền cho GitHub Actions "giả danh" SA của runner
# Đây là bước quan trọng nhất
resource "google_service_account_iam_member" "github_runner_impersonation" {
  # GSA của runner mà chúng ta đã tạo ở lần trước
  service_account_id = google_service_account.github_runner_sa.name
  role               = "roles/iam.workloadIdentityUser"

  # Định danh của GitHub Actions
  # Cú pháp: "principalSet://iam.googleapis.com/{POOL_ID}/attribute.repository/{ORG_NAME}/{REPO_NAME}"
 #member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/your-github-org/your-repo-name"
 member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/tinhnguyen0110/job-crawl-pipeline"

}

# Cấp quyền để lấy access token
resource "google_service_account_iam_member" "github_token_creator" {
  service_account_id = google_service_account.github_runner_sa.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/tinhnguyen0110/job-crawl-pipeline"
}

# Quyền deploy lên GKE
resource "google_project_iam_member" "runner_gke_developer" {
  project = var.project_id
  role    = "roles/container.admin"
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

#========= cấp quyền cho External Secrets Operator ===========
resource "google_service_account" "eos_sa" {
  project      = var.project_id
  account_id   = "eos-sa-crawl2insight"
  display_name = "Service Account for External Secrets Operator"
}

# Liên kết GSA của eos với KSA trong cluster
resource "google_service_account_iam_member" "eos_workload_binding" {
  service_account_id = google_service_account.eos_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[external-secrets/eos-ksa]"
}

resource "google_project_iam_member" "eos_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.eos_sa.email}"
}

#========= cấp quyền cho GKE Node ============
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

resource "google_secret_manager_secret_iam_member" "airflow_fernet_key_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.airflow_fernet_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.airflow_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "airflow_variables_litellm_api_key_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.airflow_variables_litellm_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.airflow_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "airflow_connections_cloud_sql_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.airflow_connections_cloud_sql.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.airflow_sa.email}"
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
  secret_id = google_secret_manager_secret.litellm_openai_api_keys.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.litellm_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "litellm_ui_credentials_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.litellm_ui_credentials.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.litellm_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "litellm_master_key_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.litellm_master_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.litellm_sa.email}"
}

# Liên kết GSA của app với KSA trong cluster
resource "google_service_account_iam_member" "litellm_workload_binding" {
  service_account_id = google_service_account.litellm_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[platform-services/litellm-ksa]"
}