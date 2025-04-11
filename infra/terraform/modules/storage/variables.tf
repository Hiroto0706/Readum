variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
}

variable "storage_bucket_name" {
  description = "Cloud Storageバケット名"
  type        = string
}

variable "region" {
  description = "バケットのリージョン"
  type        = string
}
