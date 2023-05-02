variable "project_id" {
  description = "The name of the project"
  type        = string
  default     = "gcp-project-id"
}

variable "region" {
  description = "The default compute region"
  type        = string
  default     = "europe-west4"
}

variable "zone" {
  description = "The default compute zone"
  type        = string
  default     = "europe-west4-a"
}

variable "repository" {
  description = "The name of the Artifact Registry repository to be created"
  type        = string
  default     = "docker-repository"
}

variable "docker_image" {
  description = "The name of the Docker image in the Artifact Registry repository to be deployed to Cloud Run"
  type        = string
  default     = "my-api"
}