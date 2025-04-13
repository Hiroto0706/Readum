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

variable "storage_roles" {
  description = "ストレージに付与するロール一覧"
  type        = list(string)
}

variable "service_account_email" {
  description = "サービスアカウントのメールアドレス"
  type        = string
}
