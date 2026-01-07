from typing import Optional, Union

import numpy as np
import pandas as pd

#####

FEATURE_MAP = [
    ("standard_styles", "style_"),
    ("country_of_origin", "country_"),
    ("_note_quality", "flavor_category_"),
]


def get_binary_values(
    df: pd.DataFrame,
    feature: tuple,
    dtype: Optional[Union[int, float, bool]] = int,  # NOQA
) -> pd.DataFrame:
    """
    Translates a categorical column into a binary column

    Args:
        df: Pandas DataFrame
        feature: A (column name, prefix) pair, defined in config
        dtype: One of `int` `float` or `bool`

    Returns:
        Pandas DataFrame of binary values
    """

    # Get binary values for given feature
    _tmp = pd.get_dummies(df[feature[0]], prefix=feature[1], dtype=dtype)

    # Drop column in base dataframe
    df.drop(feature[0], axis=1, inplace=True)

    # Clean up columns
    _tmp.columns = [x.lower().replace(" ", "").replace("-", "_") for x in _tmp.columns]  # NOQA

    return _tmp


def z_transform_by_year(
    df: pd.DataFrame, target_column: str = "rating"
) -> pd.DataFrame:
    """
    Applies a z-transform to the target column for a given year (e.g., `rating`).
    This is meant to account for differences in average ratings by year (and differences
    in rating distributions by year).

    Args:
        df: Pandas DataFrame
        target_column: The target column to z-transform

    Returns:
        Pandas DataFrame with an additional `_z_rating` column
    """

    _mean = np.mean(df[target_column])
    _std = np.std(df[target_column])

    df["_z_rating"] = df[target_column].apply(lambda x: (x - _mean) / _std)

    return df


def model(dbt, session):
    df = dbt.ref("stg__metadata").toPandas()

    # NOTE - We calculate the average rating per year in the "metadata"
    # staging model - this is used to create a feature representing
    # the distance from the average rating for that year
    df["_rating_distance_from_average"] = np.abs(
        df["rating"] - df["average_rating_by_year"]
    )

    # TODO - See if we can't model some of the semantic information in reviews
    df.drop("review", axis=1, inplace=True)

    # Create binary maps for categorical features and append
    # them to the main dataframe in memory
    binary_maps = [df]
    for feature in FEATURE_MAP:
        binary_maps.append(get_binary_values(df=df, feature=feature))

    # Concatenate all binary maps into a single dataframe
    df = pd.concat(binary_maps, axis=1)

    # FIXME - There's an efficiency problem here
    year_dfs = []
    for year in df["source_year"].unique():
        year_df = df.loc[df["source_year"] == year].reset_index(drop=True)
        year_dfs.append(z_transform_by_year(df=year_df))

    return pd.concat(year_dfs, axis=0).reset_index(drop=True)
