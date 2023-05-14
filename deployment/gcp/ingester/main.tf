terraform {
  cloud {
    organization = "ForwardOperators"

    workspaces {
      name = "ingester"
    }
  }
}


terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  alias = "impersonation"
  scopes = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
  ]
}

data "google_service_account_access_token" "default" {
  provider               = google.impersonation
  target_service_account = "arxiv-ingester@arxiv-production-383615.iam.gserviceaccount.com"
  scopes                 = ["userinfo-email", "cloud-platform"]
  lifetime               = "1200s"
}


provider "google" {
  project         = "arxiv-production-383615"
  access_token    = data.google_service_account_access_token.default.access_token
  request_timeout = "60s"
}

resource "google_compute_instance" "default" {
  name         = "ingester-1"
  machine_type = "n1-highmem-2"
  zone         = "europe-west4-a"

  metadata = {
    enable-oslogin = "TRUE"
  }
  boot_disk {
    initialize_params {
      image = "projects/click-to-deploy-images/global/images/tf-2-11-cu113-v20230502-debian-10-py37"
    }
  }

  network_interface {
    network = "default"

    access_config {
      # Include this section to give the VM an external IP address
    }
  }
}
