
output "frontend_url" {
  description = "フロントエンドのURL"
  value       = google_cloud_run_v2_service.readum_frontend.uri
}

output "backend_url" {
  description = "バックエンドのURL"
  value       = google_cloud_run_v2_service.readum_backend.uri
}

output "frontend_service_id" {
  description = "フロントエンドサービスのID"
  value       = google_cloud_run_v2_service.readum_frontend.id
}

output "backend_service_id" {
  description = "バックエンドサービスのID"
  value       = google_cloud_run_v2_service.readum_backend.id
}
