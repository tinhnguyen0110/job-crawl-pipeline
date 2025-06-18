output "gke_cluster_name" {
  description = "GKE cluster name."
  value       = google_container_cluster.primary.name
}

output "gke_cluster_endpoint" {
  description = "GKE cluster endpoint."
  value       = google_container_cluster.primary.endpoint
  sensitive   = true
}

output "kubeconfig_command" {
  description = "Command to configure kubectl for the created GKE cluster."
  value       = "gcloud container clusters get-credentials ${google_container_cluster.primary.name} --region ${google_container_cluster.primary.location} --project ${var.project_id}"
}