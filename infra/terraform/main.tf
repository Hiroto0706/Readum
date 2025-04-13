# サービスアカウント
data "google_service_account" "service_account" {
  account_id = var.service_account_id
  project    = var.project_id
}

# ネットワークモジュール
module "networking" {
  source = "./modules/networking"

  project_id     = var.project_id
  region         = var.region
  network_name   = var.network_name
  connector_name = var.connector_name
}

# Storageモジュール
module "storage" {
  source = "./modules/storage"

  project_id            = var.project_id
  storage_bucket_name   = var.storage_bucket_name
  region                = var.region
  storage_roles         = var.storage_roles
  service_account_email = data.google_service_account.service_account.email
}

# Cloud Runモジュール
module "cloudrun" {
  source = "./modules/cloudrun"

  project_id            = var.project_id
  region                = var.region
  frontend_service_name = var.frontend_service_name
  backend_service_name  = var.backend_service_name
  service_account_email = data.google_service_account.service_account.email
  vpc_connector_id      = module.networking.vpc_connector_id

  # 環境変数
  # フロントエンド環境変数
  API_ENDPOINT                   = var.API_ENDPOINT
  NEXT_PUBLIC_MAX_QUESTION_COUNT = var.NEXT_PUBLIC_MAX_QUESTION_COUNT
  NEXT_PUBLIC_MIN_QUESTION_COUNT = var.NEXT_PUBLIC_MIN_QUESTION_COUNT
  DISABLED_CRAWL                 = var.DISABLED_CRAWL

  # バックエンド環境変数
  ENV                   = var.ENV
  ALLOW_ORIGIN          = var.ALLOW_ORIGIN
  GPT_MODEL             = var.GPT_MODEL
  TEXT_EMBEDDINGS_MODEL = var.TEXT_EMBEDDINGS_MODEL
  additional_env_vars   = var.additional_env_vars

  depends_on = [
    module.networking,
    module.storage,
  ]
}
