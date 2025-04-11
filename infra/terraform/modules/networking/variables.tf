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

variable "subnet_name" {
  description = "サブネット名"
  type        = string
}

variable "subnet_ip_cidr_range" {
  description = "サブネットのCIDR範囲"
  type        = string
}

variable "connector_name" {
  description = "VPCアクセスコネクタ名"
  type        = string
}
