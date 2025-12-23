"""
This model fits a linear regression to predict z-transformed ratings
based on selected features from the staging feature selection model.
"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#####


def model(dbt, session):
    """
    `dbt` and `session` are required parameters for all
    dbt-python models
    """

    df = dbt.ref("stg__feature_selection").toPandas()

    # Drop null values
    test_df = df.loc[df["rating"].notna()]

    # Isolate the features and the target variable
    _features = ["proof", "_note_index"] + [x for x in df.columns if "__" in x]
    _x_values = test_df[_features]
    _y_values = test_df["_z_rating"]

    # Split the dataframe into training subsets (so as not to overfit)
    X_train, _, y_train, _ = train_test_split(
        _x_values, _y_values, test_size=0.35, random_state=54
    )

    # Fit the regression model
    lr = LinearRegression().fit(X=X_train, y=y_train)

    # We'll use the fitted regression model to predict ratings on the dataset
    _prediction_set = df[_features]
    _predicted_vals = lr.predict(_prediction_set)

    # Assign those predicted values to a new column
    df["_predicted_z_rating"] = _predicted_vals

    df = df.loc[
        :,
        [
            "dbt_id",
            "profile_id",
            "_z_rating",
            "_predicted_z_rating",
            "_note_index",
        ],
    ]

    return df
