###########################################################
# フロントエンド
###########################################################
resource "google_cloud_run_v2_service" "readum_frontend" {
  name     = var.frontend_service_name
  location = var.region

  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers[0].image,
    ]
  }

  template {
    scaling {
      max_instance_count = 2
      min_instance_count = 0
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/readum-repo/readum-frontend:latest"

      resources {
        cpu_idle = true
        limits = {
          cpu    = "1000m"
          memory = "256Mi"
        }
      }

      # 環境変数
      env {
        name  = "NODE_ENV"
        value = "production"
      }
      env {
        name  = "API_ENDPOINT"
        value = var.API_ENDPOINT
      }
      env {
        name  = "NEXT_PUBLIC_MAX_QUESTION_COUNT"
        value = var.NEXT_PUBLIC_MAX_QUESTION_COUNT
      }
      env {
        name  = "NEXT_PUBLIC_MIN_QUESTION_COUNT"
        value = var.NEXT_PUBLIC_MIN_QUESTION_COUNT
      }
      env {
        name  = "DISABLED_CRAWL"
        value = var.DISABLED_CRAWL
      }
    }

    # vpc_access {
    #   connector = var.vpc_connector_id
    #   egress    = "ALL_TRAFFIC"
    # }

    # サービスアカウント
    service_account = var.service_account_email
  }
}

# フロントエンドのIAMポリシー
resource "google_cloud_run_v2_service_iam_member" "frontend_access" {
  name     = google_cloud_run_v2_service.readum_frontend.name
  location = google_cloud_run_v2_service.readum_frontend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

###########################################################
# バックエンド
###########################################################
resource "google_cloud_run_v2_service" "readum_backend" {
  name     = var.backend_service_name
  location = var.region
  # ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY" # VPC内部からのアクセスのみ許可
  ingress = "INGRESS_TRAFFIC_ALL" # すべてのトラフィックを許可

  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers[0].image,
    ]
  }

  template {
    scaling {
      max_instance_count = 2
      min_instance_count = 0
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/readum-repo/readum-backend:latest"

      resources {
        cpu_idle = true
        limits = {
          cpu    = "1000m"
          memory = "256Mi"
        }
      }

      # 環境変数
      env {
        name  = "ENV"
        value = var.ENV
      }
      env {
        name  = "ALLOW_ORIGIN"
        value = var.ALLOW_ORIGIN
      }
      env {
        name  = "USE_LANGGRAPH"
        value = var.USE_LANGGRAPH
      }
      env {
        name  = "GPT_MODEL"
        value = var.GPT_MODEL
      }
      env {
        name  = "TEXT_EMBEDDINGS_MODEL"
        value = var.TEXT_EMBEDDINGS_MODEL
      }
      dynamic "env" {
        for_each = var.additional_env_vars
        content {
          name  = env.key
          value = env.value
        }
      }

      env {
        name  = "OPENAI_API_KEY"
        value = local.OPENAI_API_KEY
      }
      env {
        name  = "LANGCHAIN_API_KEY"
        value = local.LANGCHAIN_API_KEY
      }
      env {
        name  = "FIRECRAWL_API_KEY"
        value = local.FIRECRAWL_API_KEY
      }
    }

    # vpc_access {
    #   connector = var.vpc_connector_id
    #   egress    = "ALL_TRAFFIC"
    # }

    # サービスアカウント
    service_account = var.service_account_email
  }
}

# バックエンドのIAMポリシー - 内部アクセスのみ（サービスアカウントのみアクセス可能）
resource "google_cloud_run_v2_service_iam_member" "backend_access" {
  name     = google_cloud_run_v2_service.readum_backend.name
  location = google_cloud_run_v2_service.readum_backend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
