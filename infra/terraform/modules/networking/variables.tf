variable "project_id" {
  description = "GCPプロジェクトID"
  type        = string
}

variable "region" {
  description = "デプロイするリージョン"
  type        = string
}

variable "network_name" {
  description = "VPCネットワーク名"
  type        = string
}

variable "connector_name" {
  description = "VPCアクセスコネクタ名"
  type        = string
}
