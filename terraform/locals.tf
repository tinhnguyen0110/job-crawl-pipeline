### ssh user for git sync airflow
locals {
  gitsync_ssh_private_key = file("airflow-gitsync")
}