# APIの有効化
locals {
  services = [
    "run.googleapis.com",
    "vpcaccess.googleapis.com",
    "compute.googleapis.com",
    "iam.googleapis.com",
    "storage.googleapis.com",
  ]
}

resource "google_project_service" "services" {
  for_each = toset(local.services)

  project = var.project_id
  service = each.value

  disable_dependent_services = true
  disable_on_destroy         = false
}

# ネットワークモジュール
module "networking" {
  source = "./modules/networking"

  project_id           = var.project_id
  region               = var.region
  network_name         = var.network_name
  subnet_name          = var.subnet_name
  subnet_ip_cidr_range = var.subnet_ip_cidr_range
  connector_name       = var.connector_name

  depends_on = [google_project_service.services]
}

# IAMモジュール
module "iam" {
  source = "./modules/iam"

  project_id                   = var.project_id
  service_account_id           = var.service_account_id
  service_account_display_name = var.service_account_display_name
  storage_bucket_name          = module.storage.storage_bucket_name
  storage_roles                = var.storage_roles
  project_roles                = var.project_roles
}

# Storageモジュール
module "storage" {
  source = "./modules/storage"

  project_id          = var.project_id
  storage_bucket_name = var.storage_bucket_name
  region              = var.region

  depends_on = [google_project_service.services]
}

# Cloud Runモジュール
module "cloudrun" {
  source = "./modules/cloudrun"

  project_id            = var.project_id
  region                = var.region
  frontend_service_name = var.frontend_service_name
  backend_service_name  = var.backend_service_name
  service_account_email = module.iam.service_account_email
  vpc_connector_id      = module.networking.vpc_connector_id

  depends_on = [
    google_project_service.services,
    module.networking,
    module.iam
  ]
}
