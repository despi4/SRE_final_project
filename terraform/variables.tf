
variable "project_name" {
  description = "Project name used for Docker resources"
  type        = string
  default     = "fastapi-sre"
}

variable "docker_host" {
  description = "Docker host connection string"
  type        = string
  default     = "unix:///var/run/docker.sock"
}

variable "api_port" {
  description = "External port for FastAPI service"
  type        = number
  default     = 8000
}

variable "prometheus_port" {
  description = "External port for Prometheus"
  type        = number
  default     = 9090
}

variable "grafana_port" {
  description = "External port for Grafana"
  type        = number
  default     = 3001
}

variable "alertmanager_port" {
  description = "External port for Alertmanager"
  type        = number
  default     = 9093
}

variable "environment" {
  description = "Application environment"
  type        = string
  default     = "production"
}