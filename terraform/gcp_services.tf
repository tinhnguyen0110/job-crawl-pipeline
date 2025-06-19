# 1. Tạo Artifact Registry để chứa Docker images (thay thế cho GCR)
resource "google_artifact_registry_repository" "main_repo" {
  provider      = google-beta
  project       = var.project_id
  location      = var.region
  repository_id = "crawl2insight-repo" # Tên kho chứa của bạn
  description   = "Main Docker repository for the Crawl2Insight project"
  format        = "DOCKER"
}

# 2. Tạo các "vỏ" secret trong Secret Manager
resource "google_secret_manager_secret" "airflow_fernet_key" {
  project   = var.project_id
  secret_id = "airflow-fernet-key"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "litellm_master_key" {
  project   = var.project_id
  secret_id = "litellm-master-key"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "litellm_openai_api_keys" {
  project   = var.project_id
  secret_id = "litellm-openai-api-keys"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "litellm_ui_credentials" {
  project   = var.project_id
  secret_id = "litellm-ui-credentials"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "gitsync_ssh_key" {
  project   = var.project_id
  secret_id = "gitsync-ssh-key"
  replication {
    automatic = true
  }
}

# 3. Thêm phiên bản đầu tiên cho secret (giá trị thực)
# !!! QUAN TRỌNG: Hãy thay thế các giá trị placeholder bằng giá trị thật của bạn
resource "google_secret_manager_secret_version" "airflow_fernet_key_v1" {
  secret      = google_secret_manager_secret.airflow_fernet_key.id
  secret_data = "PpwOpKTKaHYo-TuiwCIMSwxNmBJknIf4rV5KctQ_8-k="
}

resource "google_secret_manager_secret_version" "litellm_openai_api_keys_v1" {
  secret      = google_secret_manager_secret.litellm_openai_api_keys.id
  secret_data = jsonencode({
    GOOGLE_API_KEY = var.google_api_key
  })
}

resource "google_secret_manager_secret_version" "litellm_master_key_v1" {
  secret      = google_secret_manager_secret.litellm_master_key.id
  secret_data = var.litellm_master_key
}

resource "google_secret_manager_secret_version" "litellm_ui_credentials_v1" {
  secret      = google_secret_manager_secret.litellm_ui_credentials.id
  secret_data = jsonencode({
    username = "admin"
    password = sensitive("admin123")
  })
}

resource "google_secret_manager_secret_version" "gitsync_ssh_key_v1" {
  secret      = google_secret_manager_secret.gitsync_ssh_key.id
  secret_data = var.gitsync_ssh_private_key # Sử dụng biến đã khai báo trong variables.tf
}