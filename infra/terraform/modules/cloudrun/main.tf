###########################################################
# フロントエンド
###########################################################
# フロントエンド Cloud Run サービス
resource "google_cloud_run_service" "frontend" {
  name     = var.frontend_service_name
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/${var.frontend_service_name}:latest"

        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }

        # 環境変数
        env {
          name  = "NODE_ENV"
          value = "production"
        }
      }

      # サービスアカウント
      service_account_name = var.service_account_email
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "3"
        # VPCアクセスコネクタを設定
        "run.googleapis.com/vpc-access-connector" = var.vpc_connector_id
        # すべてのトラフィックをVPCを通す
        "run.googleapis.com/vpc-access-egress" = "all-traffic"
      }
    }
  }

  # トラフィックルーティング
  traffic {
    percent         = 100
    latest_revision = true
  }
}

# フロントエンドのIAMポリシー
resource "google_cloud_run_service_iam_member" "frontend_access" {
  service  = google_cloud_run_service.frontend.name
  location = google_cloud_run_service.frontend.location
  role     = "roles/run.invoker"
  member   = var.frontend_is_public ? "allUsers" : "serviceAccount:${var.service_account_email}"
}

###########################################################
# バックエンド
###########################################################
# バックエンド Cloud Run サービス
resource "google_cloud_run_service" "backend" {
  name     = var.backend_service_name
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/${var.backend_service_name}:latest"

        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }

        # 環境変数
        env {
          name  = "PYTHON_ENV"
          value = "production"
        }
      }

      # サービスアカウント
      service_account_name = var.service_account_email
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "1"
        "autoscaling.knative.dev/maxScale" = "3"
        # VPCアクセスコネクタを設定
        "run.googleapis.com/vpc-access-connector" = var.vpc_connector_id
        # すべてのトラフィックをVPCを通す
        "run.googleapis.com/vpc-access-egress" = "all-traffic"
      }
    }
  }

  # トラフィックルーティング
  traffic {
    percent         = 100
    latest_revision = true
  }
}

# バックエンドのIAMポリシー - 内部アクセスのみ（サービスアカウントのみアクセス可能）
resource "google_cloud_run_service_iam_member" "backend_access" {
  service  = google_cloud_run_service.backend.name
  location = google_cloud_run_service.backend.location
  role     = "roles/run.invoker"
  member   = "serviceAccount:${var.service_account_email}"
}
