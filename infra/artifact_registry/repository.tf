resource "google_artifact_registry_repository" "my-repo" {
  project       = "ian-dev-444015"
  location      = "us-central1"
  repository_id = "whiskey-ml"
  description   = "Whiskey ML Artifact Registry"
  format        = "DOCKER"
}
