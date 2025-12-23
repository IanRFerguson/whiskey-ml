resource "google_dataproc_cluster" "ml_cluster" {
  name   = "whiskey-ml-cluster"
  region = "us-central1"

  cluster_config {
    staging_bucket = google_storage_bucket.dataproc_staging_bucket.name

    master_config {
      num_instances = 1
      machine_type  = "e2-standard-2"

      disk_config {
        boot_disk_type    = "pd-ssd"
        boot_disk_size_gb = 100
      }
    }

    worker_config {
      num_instances = 4
      machine_type  = "n2-standard-4"

      disk_config {
        boot_disk_type    = "pd-ssd"
        boot_disk_size_gb = 100
      }
    }

    software_config {
      image_version = "2.2-debian11"
    }
  }
}
