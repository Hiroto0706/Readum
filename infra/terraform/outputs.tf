output "frontend_url" {
  description = "フロントエンドのURL"
  value       = module.cloudrun.frontend_url
}

output "backend_url" {
  description = "バックエンドのURL"
  value       = module.cloudrun.backend_url
}

# output "vpc_connector_id" {
#   description = "VPCアクセスコネクタのID"
#   value       = module.networking.vpc_connector_id
# }

output "storage_bucket_url" {
  description = "ストレージバケットのURL"
  value       = module.storage.storage_bucket_url
}
