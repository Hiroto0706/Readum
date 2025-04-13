resource "google_secret_manager_secret" "main" {
  secret_id = var.secret_id

  labels = {
    "managed-by" = "terraform"
  }

  lifecycle {
    prevent_destroy = true
  }

  replication {
    auto {}
  }
}
