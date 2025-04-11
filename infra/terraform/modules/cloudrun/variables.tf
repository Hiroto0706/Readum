variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
}

variable "region" {
  description = "デプロイするリージョン"
  type        = string
}

variable "frontend_service_name" {
  description = "フロントエンドのCloud Run名"
  type        = string
}

variable "backend_service_name" {
  description = "バックエンドのCloud Run名"
  type        = string
}

variable "service_account_email" {
  description = "サービスアカウントのメールアドレス"
  type        = string
}

variable "vpc_connector_id" {
  description = "VPCアクセスコネクタのID"
  type        = string
}

variable "frontend_is_public" {
  description = "フロントエンドを公開するかどうか"
  type        = bool
  default     = true
}
