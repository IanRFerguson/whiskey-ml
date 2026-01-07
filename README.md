# Modeling Whiskey Ratings

This is a Machine Learning pipeline that predicts the overall rating of a whiskey based on its flavor profile, proof, and style.

## Pipeline Details
* I've filled out a Google Sheet with the metadata and reviews of 24 different whiskeys from around the world
* This raw data is represented in BigQuery as a Connected Sheet - this serves as the input data in our `dbt` project
* The transformations *and* the applied Machine Learning all occur seamlessly in the same `dbt` pipeline
  * The `staging` layer reshapes the data to prepare it for modeling
  * The `production` layer fits and applies the regression model

## Model Results
The regression model is actually predicting what I would rate the beverage 5 times over - one prediction per tasting note in order. Those ratings are then averaged to give us a compositie estimated rating. We can interpret narrower boxplots below as beverages that were more consistently predicted in this framework on a flavor by flavor basis: 

<img src="./plots/2026/3d_scatterplot__by_cluster.png" width="45%">

## Setup
You can run all of the necessary `dbt` commands directly from the Docker container - just run `make shell` to initialize the container and execute `dbt build` directly from the command line.

Run `make pipeline` to run the `dbt` steps and regenerate the plots you see here.

The only requisitie cloud infrastructure required is a Google Storage bucket - this can be modified in [the dbt profile YAML](./src/profiles.yml), and is only required to unload the PySpark batches as they run on GKE clusters.