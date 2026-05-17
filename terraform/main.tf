resource "docker_network" "sre_network" {
  name = "${var.project_name}-network"
}

resource "docker_volume" "grafana_data" {
  name = "${var.project_name}-grafana-data"
}

resource "docker_image" "fastapi_app" {
  name = "${var.project_name}-app:latest"

  build {
    context    = "${path.module}/.."
    dockerfile = "Dockerfile"
  }
}

resource "docker_image" "prometheus" {
  name = "prom/prometheus:latest"
}

resource "docker_image" "grafana" {
  name = "grafana/grafana:latest"
}

resource "docker_image" "alertmanager" {
  name = "prom/alertmanager:latest"
}

resource "local_file" "prometheus_config" {
  filename = "${path.module}/generated/prometheus.yml"

  content = <<EOT
global:
  scrape_interval: 15s

rule_files:
  - /etc/prometheus/alert_rules.yml

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - "alertmanager:9093"

scrape_configs:
  - job_name: "fastapi-service"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["fastapi-app:8000"]

  - job_name: "prometheus"
    static_configs:
      - targets: ["prometheus:9090"]
EOT
}

resource "local_file" "alert_rules" {
  filename = "${path.module}/generated/alert_rules.yml"

  content = <<EOT
groups:
  - name: fastapi-alerts
    rules:
      - alert: FastAPIServiceDown
        expr: up{job="fastapi-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "FastAPI service is down"
          description: "Prometheus cannot scrape metrics from the FastAPI service."

      - alert: HighRequestLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High request latency"
          description: "95th percentile latency is higher than 500ms."

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate"
          description: "FastAPI service has too many 5xx errors."
EOT
}

resource "local_file" "alertmanager_config" {
  filename = "${path.module}/generated/alertmanager.yml"

  content = <<EOT
global:
  resolve_timeout: 5m

route:
  receiver: "default"

receivers:
  - name: "default"
EOT
}

resource "docker_container" "fastapi_app" {
  name  = "fastapi-app"
  image = docker_image.fastapi_app.image_id

  restart = "unless-stopped"

  networks_advanced {
    name = docker_network.sre_network.name
  }

  ports {
    internal = 8000
    external = var.api_port
  }

  env = [
    "ENVIRONMENT=${var.environment}"
  ]
}

resource "docker_container" "alertmanager" {
  name  = "alertmanager"
  image = docker_image.alertmanager.image_id

  restart = "unless-stopped"

  networks_advanced {
    name = docker_network.sre_network.name
  }

  ports {
    internal = 9093
    external = var.alertmanager_port
  }

  volumes {
    host_path      = abspath(local_file.alertmanager_config.filename)
    container_path = "/etc/alertmanager/alertmanager.yml"
    read_only      = true
  }

  command = [
    "--config.file=/etc/alertmanager/alertmanager.yml"
  ]
}

resource "docker_container" "prometheus" {
  name  = "prometheus"
  image = docker_image.prometheus.image_id

  restart = "unless-stopped"

  networks_advanced {
    name = docker_network.sre_network.name
  }

  ports {
    internal = 9090
    external = var.prometheus_port
  }

  volumes {
    host_path      = abspath(local_file.prometheus_config.filename)
    container_path = "/etc/prometheus/prometheus.yml"
    read_only      = true
  }

  volumes {
    host_path      = abspath(local_file.alert_rules.filename)
    container_path = "/etc/prometheus/alert_rules.yml"
    read_only      = true
  }

  command = [
    "--config.file=/etc/prometheus/prometheus.yml"
  ]

  depends_on = [
    docker_container.fastapi_app,
    docker_container.alertmanager
  ]
}

resource "docker_container" "grafana" {
  name  = "grafana"
  image = docker_image.grafana.image_id

  restart = "unless-stopped"

  networks_advanced {
    name = docker_network.sre_network.name
  }

  ports {
    internal = 3000
    external = var.grafana_port
  }

  volumes {
    volume_name    = docker_volume.grafana_data.name
    container_path = "/var/lib/grafana"
  }

  env = [
    "GF_SECURITY_ADMIN_USER=admin",
    "GF_SECURITY_ADMIN_PASSWORD=admin"
  ]

  depends_on = [
    docker_container.prometheus
  ]
}