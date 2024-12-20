terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.9.0"
    }
  }
}

provider "google" {
  project = "ian-dev-444015"
}

resource "google_dataproc_cluster" "dev_cluster" {
  name      = "dev-cluster"
  region    = "us-central1"

  cluster_config {
    staging_bucket = google_storage_bucket.dev_bucket.id
    temp_bucket = google_storage_bucket.dev_bucket.id

    gce_cluster_config {
      internal_ip_only = false
    }

    master_config {
      num_instances = 1
      machine_type  = "e2-medium"
      disk_config {
        boot_disk_type    = "pd-ssd"
        boot_disk_size_gb = 30
      }
    }

    worker_config {
      num_instances = 4
      machine_type = "e2-medium"
      disk_config {
        boot_disk_type = "pd-ssd"
        boot_disk_size_gb = 1000
      }
    }
  }
}

resource "google_storage_bucket" "dev_bucket" {
  name      = "whiskey-dbt-dev"
  location  = "US"
}