# サービスアカウント
resource "google_service_account" "service_account" {
  account_id   = var.service_account_id
  display_name = var.service_account_display_name
  project      = var.project_id
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
  service_account_email = google_service_account.service_account.email
}

# Cloud Runモジュール
module "cloudrun" {
  source = "./modules/cloudrun"

  project_id            = var.project_id
  region                = var.region
  frontend_service_name = var.frontend_service_name
  backend_service_name  = var.backend_service_name
  service_account_email = google_service_account.service_account.email
  vpc_connector_id      = module.networking.vpc_connector_id

  depends_on = [
    module.networking,
    module.storage,
  ]
}
