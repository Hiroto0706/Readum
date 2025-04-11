output "frontend_url" {
  description = "フロントエンドのURL"
  value       = google_cloud_run_service.frontend.status[0].url
}

output "backend_url" {
  description = "バックエンドのURL"
  value       = google_cloud_run_service.backend.status[0].url
}

output "frontend_service_id" {
  description = "フロントエンドサービスのID"
  value       = google_cloud_run_service.frontend.id
}

output "backend_service_id" {
  description = "バックエンドサービスのID"
  value       = google_cloud_run_service.backend.id
}
