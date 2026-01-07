resource "google_storage_bucket" "dataproc_staging_bucket" {
  project       = "ian-dev-444015"
  name          = "whiskey-ml-dataproc-staging-bucket"
  location      = "US"
  force_destroy = true
}

# NOTE - This techincally isn't a "bucket" resource, but it is related to general
# bucket access. Might move this to an IAM file if needed
resource "google_project_iam_binding" "dataproc_staging_bucket_iam" {
  project = "ian-dev-444015"
  role    = "roles/storage.objectAdmin"
  members = [
    "serviceAccount:817201868807-compute@developer.gserviceaccount.com"
  ]
}
