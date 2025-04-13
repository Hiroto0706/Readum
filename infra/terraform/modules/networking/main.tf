# VPCネットワーク
resource "google_compute_network" "vpc_network" {
  name = var.network_name
}

# VPCアクセスコネクタ
resource "google_vpc_access_connector" "connector" {
  name          = var.connector_name
  region        = var.region
  network       = google_compute_network.vpc_network.id
  ip_cidr_range = "10.20.0.0/28"
}
