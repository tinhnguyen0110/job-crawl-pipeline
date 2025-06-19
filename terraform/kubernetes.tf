# kubernetes.tf

# Lấy thông tin GKE cluster đã có để xác thực provider
data "google_container_cluster" "primary" {
  name     = var.gke_cluster_name
  location = var.region
  project  = var.project_id
}

# Cấu hình provider Kubernetes để Terraform có thể thao tác với GKE
provider "kubernetes" {
  host                   = "https://{data.google_container_cluster.primary.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(data.google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
}

# 1. Tạo các Namespace mới
resource "kubernetes_namespace" "airflow_ns" {
  metadata {
    name = "airflow"
  }
}

resource "kubernetes_namespace" "platform_services_ns" {
  metadata {
    name = "platform-services" # Namespace cho LiteLLM
  }
}

resource "kubernetes_namespace" "secret_ns" {
  metadata {
    name = "external-secrets" # Namespace cho External Secrets Operator
  }
}

# 2. Tạo Kubernetes Service Accounts (KSA) cho các ứng dụng
resource "kubernetes_service_account" "airflow_ksa" {
  metadata {
    name      = "airflow-ksa"
    namespace = kubernetes_namespace.airflow_ns.metadata[0].name
    # Liên kết KSA này với GSA của Airflow
    annotations = {
      "iam.gke.io/gcp-service-account" = google_service_account.airflow_sa.email
    }
  }
}

resource "kubernetes_service_account" "litellm_ksa" {
  metadata {
    name      = "litellm-ksa"
    namespace = kubernetes_namespace.platform_services_ns.metadata[0].name
    # Liên kết KSA này với GSA của LiteLLM
    annotations = {
      "iam.gke.io/gcp-service-account" = google_service_account.litellm_sa.email
    }
  }
}

resource "kubernetes_service_account" "eos_ksa" {
  metadata {
    name      = "eos-ksa"
    namespace = kubernetes_namespace.platform_services_ns.metadata[0].name
    # Liên kết KSA này với GSA của EOS
    annotations = {
      "iam.gke.io/gcp-service-account" = google_service_account.eos_sa.email
    }
  }
}

# 3. Thiết lập liên kết Workload Identity (cho phép KSA "giả danh" GSA)
resource "google_service_account_iam_member" "airflow_workload_binding" {
  service_account_id = google_service_account.airflow_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${kubernetes_namespace.airflow_ns.metadata[0].name}/${kubernetes_service_account.airflow_ksa.metadata[0].name}]"
}

resource "google_service_account_iam_member" "litellm_workload_binding" {
  service_account_id = google_service_account.litellm_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${kubernetes_namespace.platform_services_ns.metadata[0].name}/${kubernetes_service_account.litellm_ksa.metadata[0].name}]"
  }

resource "google_service_account_iam_member" "eos_workload_binding" {
  service_account_id = google_service_account.eos_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${kubernetes_namespace.secret_ns.metadata[0].name}/${kubernetes_service_account.eos_ksa.metadata[0].name}]"
  }