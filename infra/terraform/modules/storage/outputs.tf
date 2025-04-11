output "storage_bucket_name" {
  description = "バケット名"
  value       = google_storage_bucket.readum_bucket.name
}

output "storage_bucket_url" {
  description = "バケットのURL"
  value       = google_storage_bucket.readum_bucket.url
}
