"""
This model uses a clustering algorithm to segment whiskey profiles
based on selected features from the staging feature selection model.
"""

from sklearn.cluster import KMeans
import pandas as pd

#####


def collapse_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse the dataframe to only include the first note for each whiskey profile.
    This is done to ensure that each profile is represented only once in the clustering.
    """

    # We only need a handful of columns for this operation
    index_cols = ["dbt_id", "proof", "source_year"]
    df = df.loc[
        :,
        df.columns.str.contains("__") | df.columns.isin(index_cols),
    ]

    # Kind of naive approach but does work in this context
    dummy_cols = [c for c in df.columns if "__" in c]

    df_wide = df.groupby(index_cols)[dummy_cols].max().reset_index()

    return df_wide


def model(dbt, session):
    df = dbt.ref("stg__feature_selection").toPandas()

    # Filter to only include the first note for each whiskey profile
    df_wide = collapse_dataframe(df=df)

    # Isolate the features for clustering
    _features = ["proof", "source_year"] + [x for x in df_wide.columns if "__" in x]
    _x_values = df_wide[_features]

    # Fit the KMeans clustering model
    kmeans = KMeans(n_clusters=5, random_state=54)
    df_wide["_cluster_label"] = kmeans.fit_predict(_x_values)

    return df_wide.loc[
        :,
        [
            "dbt_id",
            "_cluster_label",
        ],
    ]
