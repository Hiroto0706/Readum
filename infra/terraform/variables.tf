variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
}

variable "region" {
  description = "デプロイするリージョン"
  type        = string
  default     = "asia-northeast1"
}

variable "storage_bucket_name" {
  description = "Cloud Storageバケット名"
  type        = string
}

variable "service_account_id" {
  description = "サービスアカウントID（@より前の部分）"
  type        = string
}

variable "service_account_display_name" {
  description = "サービスアカウントの表示名"
  type        = string
  default     = "Readum Service Account"
}

variable "network_name" {
  description = "VPCネットワーク名"
  type        = string
  default     = "vpc-network"
}

variable "connector_name" {
  description = "VPCアクセスコネクタ名"
  type        = string
  default     = "vpc-connector"
}

variable "frontend_service_name" {
  description = "フロントエンドのCloud Run名"
  type        = string
  default     = "readum_frontend"
}

variable "backend_service_name" {
  description = "バックエンドのCloud Run名"
  type        = string
  default     = "readum_backend"
}

variable "storage_roles" {
  description = "ストレージに付与するロール一覧"
  type        = list(string)
  default     = ["roles/storage.admin"]
}
