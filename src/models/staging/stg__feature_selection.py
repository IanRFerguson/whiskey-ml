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
    _tmp.columns = [
        x.lower().replace(" ", "").replace("-", "_") for x in _tmp.columns
    ]  # NOQA

    return _tmp


def model(dbt, session):
    df = dbt.ref("stg__metadata").toPandas()

    # Get rating distance from average
    _average_rating = np.mean(df["rating"])

    df["_rating_distance_from_average"] = df["rating"].apply(
        lambda x: x - _average_rating
    )

    df.drop("review", axis=1, inplace=True)

    binary_maps = [df]
    for feature in FEATURE_MAP:
        binary_maps.append(get_binary_values(df=df, feature=feature))

    df = pd.concat(binary_maps, axis=1)

    return df
