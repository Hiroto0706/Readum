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
  machine_type  = "e2-micro"
  max_instances = 3
  min_instances = 2
}

# Cloud Routerの作成
resource "google_compute_router" "router" {
  name    = "${var.network_name}-router"
  region  = var.region
  network = google_compute_network.vpc_network.id
}

# Cloud NATの作成
resource "google_compute_router_nat" "nat" {
  name                               = "${var.network_name}-nat"
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}
