terraform {

  cloud {
    organization = "ForwardOperators"
    workspaces {
      name = "arxivchat"
    }
  }

  required_providers {
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "4.63.1"
    }
  }
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}


# Enable API's                

# Enable IAM API
resource "google_project_service" "iam" {
  provider = google-beta
  service            = "iam.googleapis.com"
  disable_on_destroy = false
}

# Enable Artifact Registry API
resource "google_project_service" "artifactregistry" {
  provider = google-beta
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

# Enable Cloud Run API
resource "google_project_service" "cloudrun" {
  provider = google-beta
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

# Enable Cloud Resource Manager API
resource "google_project_service" "resourcemanager" {
  provider = google-beta
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
}

# This is used so there is some time for the activation of the API's to propagate through 
# Google Cloud before actually calling them.
resource "time_sleep" "wait_30_seconds" {
  create_duration = "30s"
  depends_on = [
    google_project_service.artifactregistry, 
    google_project_service.cloudrun, 
    google_project_service.resourcemanager
    ]
}



# Create Artifact Registry Repository for Docker containers
resource "google_artifact_registry_repository" "my_docker_repo" {
  provider = google-beta

  location = var.region
  repository_id = var.repository
  description = "My docker repository"
  format = "DOCKER"
  depends_on = [time_sleep.wait_30_seconds]
}

# Create a Service Account
resource "google_service_account" "docker_pusher" {
  provider = google-beta

  account_id   = "docker-pusher"
  display_name = "Docker Container Pusher"
  depends_on =[time_sleep.wait_30_seconds]
}

# Give Service Account permission to push to the Artifact Registry Repository
resource "google_artifact_registry_repository_iam_member" "docker_pusher_iam" {
  provider = google-beta

  location = google_artifact_registry_repository.my_docker_repo.location
  repository =  google_artifact_registry_repository.my_docker_repo.repository_id
  role   = "roles/artifactregistry.writer"
  member = "serviceAccount:${google_service_account.docker_pusher.email}"
  depends_on = [
    google_artifact_registry_repository.my_docker_repo, 
    google_service_account.docker_pusher
    ]
}



# Deploy image to Cloud Run
resource "google_cloud_run_service" "arxivchat" {
  provider = google-beta
  name     = "arxivchat"
  location = var.region
  template {
    spec {
        containers {
            image = "europe-central2-docker.pkg.dev/${var.project_id}/${var.repository}/${var.docker_image}"
            resources {
                limits = {
                "memory" = "4G"
                "cpu" = "2"
                }
            }
        }
    }
    metadata {
        annotations = {
            "autoscaling.knative.dev/minScale" = "0"
            "autoscaling.knative.dev/maxScale" = "2"
        }
    }
  }
  traffic {
    percent = 100
    latest_revision = true
  }
  depends_on = [google_artifact_registry_repository_iam_member.docker_pusher_iam]
}

# Create a policy that allows all users to invoke the API
data "google_iam_policy" "noauth" {
  provider = google-beta
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

# Apply the no-authentication policy to our Cloud Run Service.
resource "google_cloud_run_service_iam_policy" "noauth" {
  provider = google-beta
  location    = var.region
  project     = var.project_id
  service     = google_cloud_run_service.arxivchat.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

output "cloud_run_instance_url" {
  value = google_cloud_run_service.arxivchat.status.0.url
}