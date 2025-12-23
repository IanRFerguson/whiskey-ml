"""
This model uses a clustering algorithm to segment whiskey profiles
based on selected features from the staging feature selection model.
"""

from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

#####


def collapse_dataframe(df: DataFrame) -> DataFrame:
    """
    Collapse the dataframe to only include the first note for each whiskey profile.
    This is done to ensure that each profile is represented only once in the clustering.
    """

    # Identify columns with "__" and index columns
    index_cols = ["dbt_id", "proof", "source_year"]
    dummy_cols = [c for c in df.columns if "__" in c]
    all_cols = index_cols + dummy_cols

    # Select only relevant columns
    df_filtered = df.select(*all_cols)

    # Group by index columns and take the max of dummy columns
    agg_exprs = [F.max(c).alias(c) for c in dummy_cols]
    df_wide = df_filtered.groupBy(index_cols).agg(*agg_exprs)

    return df_wide


def model(dbt, session):
    df = dbt.ref("stg__feature_selection")

    # Filter to only include the first note for each whiskey profile
    df_wide = collapse_dataframe(df=df)

    # Isolate the features for clustering
    feature_cols = ["proof", "source_year"] + [x for x in df_wide.columns if "__" in x]

    # Assemble features into a single vector column
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    assembled_df = assembler.transform(df_wide)

    # Fit the KMeans clustering model
    kmeans = KMeans(
        k=5, seed=54, featuresCol="features", predictionCol="_cluster_label"
    )
    kmeans_model = kmeans.fit(assembled_df)

    # Apply predictions
    clustered_df = kmeans_model.transform(assembled_df)

    return clustered_df.select(
        "dbt_id",
        "_cluster_label",
    )
