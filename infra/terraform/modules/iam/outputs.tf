output "service_account_email" {
  description = "サービスアカウントのメールアドレス"
  value       = google_service_account.readum_service_account.email
}

output "service_account_id" {
  description = "サービスアカウントのID"
  value       = google_service_account.readum_service_account.id
}
