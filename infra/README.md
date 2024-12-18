# GCP Infrastructure

We need a few pieces of architecture to pull this off:
* A dataproc server to run PySpark - [docs](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/dataproc_cluster.html)
* A Cloud Storage bucket to cache / unload - [docs](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket)
* All relevant APIs activated