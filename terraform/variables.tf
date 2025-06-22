variable "litellm_master_key" {
  description = "key for LiteLLM master"
  type        = string
  sensitive   = true 
  default     = "sk-1234"
}

variable "litellm_ui_username" {
  description = "Username for LiteLLM UI"
  type        = string
}

variable "litellm_ui_password" {
  description = "Password for LiteLLM UI"
  type        = string
  sensitive   = true 
}

variable "google_api_key" {
  description = "key for Google API"
  type        = string
  sensitive   = true 
}

variable "openai_api_key" {
  description = "key for OpenAI API"
  type        = string
  sensitive   = true 
}

variable "airflow_connections_cloud_sql" {
  description = "Connection string for Airflow to connect to Cloud SQL"
  type        = string
  sensitive   = true
}

variable "airflow_variables_litellm_api_key" {
  description = "API key for LiteLLM to be used in Airflow variables"
  type        = string
  sensitive   = true
}


variable "project_id" {
  description = "The GCP project ID to deploy to."
  type        = string
  default = "alpine-figure-461007-i9"
}

variable "region" {
  description = "The GCP region to deploy GKE cluster."
  type        = string
  default     = "asia-southeast1"
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

