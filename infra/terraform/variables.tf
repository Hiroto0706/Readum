variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
}

variable "region" {
  description = "デプロイするリージョン"
  type        = string
  default     = "asia-northeast1"
}

variable "zone" {
  description = "デプロイするゾーン"
  type        = string
  default     = "asia-northeast1-a"
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

variable "subnet_name" {
  description = "サブネット名"
  type        = string
  default     = "subnet"
}

variable "subnet_ip_cidr_range" {
  description = "サブネットのCIDR範囲"
  type        = string
  default     = "10.0.0.0/28"
}

variable "connector_name" {
  description = "VPCアクセスコネクタ名"
  type        = string
  default     = "vpc-connector"
}

variable "frontend_service_name" {
  description = "フロントエンドのCloud Run名"
  type        = string
  default     = "frontend"
}

variable "backend_service_name" {
  description = "バックエンドのCloud Run名"
  type        = string
  default     = "backend"
}

variable "storage_roles" {
  description = "ストレージに付与するロール一覧"
  type        = list(string)
  default     = ["roles/storage.objectViewer"]
}

variable "project_roles" {
  description = "プロジェクトレベルで付与するロール一覧"
  type        = list(string)
  default     = ["roles/iam.serviceAccountUser"]
}
