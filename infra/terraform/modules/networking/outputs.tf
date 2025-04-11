output "vpc_network_id" {
  description = "VPCネットワークのID"
  value       = google_compute_network.vpc_network.id
}

output "subnet_id" {
  description = "サブネットのID"
  value       = google_compute_subnetwork.subnet.id
}

output "vpc_connector_id" {
  description = "VPCアクセスコネクタのID"
  value       = google_vpc_access_connector.connector.id
}
