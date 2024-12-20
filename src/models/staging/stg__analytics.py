import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans

#####

FEATURE_MAP = [
    ("standard_styles", "style_"),
    ("country_of_origin", "country_"),
    ("_note_value", "flavor_note_"),
]


def get_binary_values(df: pd.DataFrame, feature: tuple) -> pd.DataFrame:
    """
    TODO - Fill this in
    """

    # Get binary values for given feature
    _tmp = pd.get_dummies(df[feature[0]], prefix=feature[1])

    # Drop column in base dataframe
    df.drop(feature[0], axis=1, inplace=True)

    # Clean up columns
    _tmp.columns = [x.lower().replace(" ", "").replace("-", "_") for x in _tmp.columns]

    return _tmp


def _fit_kmeans_clustering(
    df: pd.DataFrame, n_clusters: int = 3, random_state: int = 0
) -> list:
    """
    TODO - Fill this in
    """

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    kmeans.fit(df)

    return [x for x in kmeans.labels_]


def _fit_linear_regression():
    pass


def model(dbt, session):
    df = dbt.ref("stg__metadata").toPandas()

    # Maintain a copy of the original data in memory
    clean_df = df.copy()

    ### Feature selection ###

    # Get rating distance from average
    _average_rating = np.mean(df["rating"])

    df["_rating_distance_from_average"] = df["rating"].apply(
        lambda x: x - _average_rating
    )

    df.drop("my_review", axis=1, inplace=True)

    ### Categorical cleanup ###

    binary_maps = [df]
    for feature in FEATURE_MAP:
        binary_maps.append(get_binary_values(df=df, feature=feature))

    df = pd.concat(binary_maps, axis=1)

    ### Apply clustering algorithm ###

    _features = [x for x in df.columns if x not in ["dbt_id", "profile_id"]]

    # Normalize all columns
    df__normalized = preprocessing.normalize(df[_features])

    # Run K-Means algorithm and assign labels
    _labels = _fit_kmeans_clustering(df=df__normalized)
    clean_df["_cluster"] = _labels

    return clean_df
