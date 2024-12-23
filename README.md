# Whiskey Tasting Machine Learning Pipeline

* Raw data is read in from a Google Sheet to a BigQuery table
* The transformations *and* the applied ML all occur in the same `dbt` pipeline
  * The `staging` layer reshapes the data to prepare it for modeling
  * The `production` layer fits and applies the regression model

## Setup
You can run all of the necessary `dbt` commands directly from the Docker container - just run `make shell`, `cd src`, and execute whatever commands you need.

The only core infrastructure required at startup is a GCS storage bucket, as the PySpark models are run on a serverless Kubernetes instance. 