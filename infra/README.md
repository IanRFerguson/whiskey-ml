# GCP Infrastructure

We need a few pieces of architecture to pull this off:
* A dataproc server to run PySpark
* A Cloud Storage bucket to cache / unload
* All relevant APIs activated