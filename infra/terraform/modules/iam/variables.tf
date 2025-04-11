variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
}

variable "service_account_id" {
  description = "サービスアカウントID（メールアドレスの@前の部分）"
  type        = string
}

variable "service_account_display_name" {
  description = "サービスアカウントの表示名"
  type        = string
  default     = "Service Account"
}

variable "storage_bucket_name" {
  description = "アクセス権を付与するストレージバケット名"
  type        = string
}

variable "storage_roles" {
  description = "ストレージに付与するロール一覧"
  type        = list(string)
}

variable "project_roles" {
  description = "プロジェクトレベルで付与するロール一覧"
  type        = list(string)
}
