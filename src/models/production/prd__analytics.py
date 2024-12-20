import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

#####


def model(dbt, session):
    df = dbt.ref("stg__feature_selection").toPandas()

    _features = ["proof", "_note_index"] + [x for x in df.columns if "__" in x]

    _x_values = df[_features]
    _y_values = df["rating"]

    X_train, X_test, y_train, y_test = train_test_split(
        _x_values, _y_values, test_size=0.35, random_state=54
    )

    lr = LinearRegression().fit(X=X_train, y=y_train)

    _prediction_set = df[_features]

    _predicted_vals = lr.predict(_prediction_set)
    df["predicted_rating"] = _predicted_vals

    df = df.loc[
        :,
        [
            "dbt_id",
            "profile_id",
            "rating",
            "predicted_rating",
            "_note_index",
        ],
    ]

    return df
