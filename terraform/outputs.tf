output "fastapi_url" {
  description = "FastAPI service URL"
  value       = "http://localhost:${var.api_port}"
}

output "health_url" {
  description = "Health endpoint URL"
  value       = "http://localhost:${var.api_port}/health"
}

output "metrics_url" {
  description = "Metrics endpoint URL"
  value       = "http://localhost:${var.api_port}/metrics"
}

output "docs_url" {
  description = "Swagger documentation URL"
  value       = "http://localhost:${var.api_port}/docs"
}

output "prometheus_url" {
  description = "Prometheus URL"
  value       = "http://localhost:${var.prometheus_port}"
}

output "grafana_url" {
  description = "Grafana URL"
  value       = "http://localhost:${var.grafana_port}"
}

output "alertmanager_url" {
  description = "Alertmanager URL"
  value       = "http://localhost:${var.alertmanager_port}"
}