output "secret_id" {
  description = "シークレットID"
  value       = google_secret_manager_secret.main.secret_id
}
