# 既存のCloud Storageバケットをインポート
# 注: 実行前に `terraform import module.storage.google_storage_bucket.readum_bucket readum` を実行する必要があります
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
