# main.tf (Improved GKE Block)
resource "google_container_cluster" "primary" {
  project  = var.project_id
  name     = var.gke_cluster_name
  location = var.region # <-- Chuyển sang Regional

  remove_default_node_pool = true
  initial_node_count       = 1

  release_channel { # <-- Dùng Release Channel
    channel = "REGULAR"
  }
  
  workload_identity_config { # <-- Bật Workload Identity
    workload_pool = "${var.project_id}.svc.id.goog"
  }
}


resource "google_container_node_pool" "primary_nodes" {
  project    = google_container_cluster.primary.project
  name       = "${google_container_cluster.primary.name}-node-pool"
  location   = google_container_cluster.primary.location
  cluster    = google_container_cluster.primary.name
  
  autoscaling { # <-- Dùng Autoscaling
    min_node_count = 1
    max_node_count = 3
  }
  
  management {
    auto_repair  = true
    auto_upgrade = true # Được quản lý bởi Release Channel
  }

  node_config {
    machine_type    = var.gke_machine_type
    service_account = google_service_account.gke_node_sa.email # <-- Dùng SA riêng
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    # spot = true # Cân nhắc dùng Spot VMs để tiết kiệm chi phí
  }
}
