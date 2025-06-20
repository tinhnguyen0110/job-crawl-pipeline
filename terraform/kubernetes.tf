# kubernetes.tf
data "google_client_config" "default" {}
# Lấy thông tin GKE cluster đã có để xác thực provider
data "google_container_cluster" "primary" {
  name     = var.gke_cluster_name
  location = var.zone
  project  = var.project_id
  depends_on = [google_container_cluster.primary]
}

# Cấu hình provider Kubernetes để Terraform có thể thao tác với GKE
provider "kubernetes" {
  host                   = "https://${data.google_container_cluster.primary.endpoint}"
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
    namespace = "external-secrets"
    # Liên kết KSA này với GSA của EOS
    annotations = {
      "iam.gke.io/gcp-service-account" = google_service_account.eos_sa.email
    }
  }
}

