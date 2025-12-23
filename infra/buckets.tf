resource "google_storage_bucket" "dataproc_staging_bucket" {
  name     = "whiskey-ml-dataproc-staging-bucket"
  location = "US"
}
