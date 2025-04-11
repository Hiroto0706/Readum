resource "google_service_account" "service_account" {
  account_id   = var.service_account_id
  display_name = var.service_account_display_name
  project      = var.project_id
}

resource "google_storage_bucket_iam_member" "storage_roles" {
  for_each = toset(var.storage_roles)

  bucket = var.storage_bucket_name
  role   = each.value
  member = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_project_iam_member" "project_roles" {
  for_each = toset(var.project_roles)

  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.service_account.email}"
}
