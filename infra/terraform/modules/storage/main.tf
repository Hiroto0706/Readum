resource "google_storage_bucket" "readum_bucket" {
  name     = var.storage_bucket_name
  location = var.region

  # バージョニングを無効化
  versioning {
    enabled = false
  }

  # 均一なアクセス制御を使用
  uniform_bucket_level_access = true

  # ライフサイクルルール
  lifecycle_rule {
    condition {
      age            = 14 # 14日後
      matches_suffix = [".json"]
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
}

# バケットへのアクセス権限
resource "google_storage_bucket_iam_member" "storage_roles" {
  for_each = toset(var.storage_roles)

  bucket = google_storage_bucket.readum_bucket.name
  role   = each.value
  member = "serviceAccount:${var.service_account_email}"
}
