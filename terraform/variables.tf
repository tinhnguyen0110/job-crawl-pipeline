variable "project_id" {
  description = "The GCP project ID to deploy to."
  type        = string
  default = "alpine-figure-461007-i9"
}

variable "region" {
  description = "The GCP region to deploy GKE cluster."
  type        = string
  default     = "asia-southeast1-a"
}

variable "zone" {
  description = "The GCP zone for the GKE cluster."
  type        = string
  default     = "asia-southeast1-a" # Ví dụ: Zone a của Singapore
}

variable "gke_cluster_name" {
  description = "Name for the GKE cluster."
  type        = string
  default     = "simple-cluster"
}

variable "gke_node_count" {
  description = "Number of nodes in the GKE cluster's default node pool."
  type        = number
  default     = 1 # Start with 1 node for simplicity
}

variable "gke_machine_type" {
  description = "Machine type for GKE nodes."
  type        = string
  default     = "e2-standard-2" # A small and cost-effective machine type
}

variable "gke_cluster_version" {
  description = "The GKE version for the master and nodes. If null, the latest available version will be used."
  type        = string
  default     = null # Let GCP pick the latest stable version
}