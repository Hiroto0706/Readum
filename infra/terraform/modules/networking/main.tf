# VPCネットワーク
resource "google_compute_network" "vpc_network" {
  name                    = var.network_name
  auto_create_subnetworks = false
}

# サブネット
resource "google_compute_subnetwork" "subnet" {
  name          = var.subnet_name
  ip_cidr_range = var.subnet_ip_cidr_range
  region        = var.region
  network       = google_compute_network.vpc_network.id
}

# VPCアクセスコネクタ
resource "google_vpc_access_connector" "connector" {
  name          = var.connector_name
  region        = var.region
  network       = google_compute_network.vpc_network.name
  ip_cidr_range = "10.8.0.0/28"

  # 最小構成
  min_instances = 2
  max_instances = 3
  machine_type  = "e2-micro"
}
