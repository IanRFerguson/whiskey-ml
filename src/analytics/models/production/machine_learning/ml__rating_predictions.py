"""
This model fits a linear regression to predict z-transformed ratings
based on selected features from the staging feature selection model.
"""

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import functions as F

#####


def model(dbt, session):
    """
    `dbt` and `session` are required parameters for all
    dbt-python models
    """

    df = dbt.ref("stg__feature_selection")

    # Drop null values
    test_df = df.filter(F.col("rating").isNotNull())

    # Isolate the features and the target variable
    feature_cols = ["proof", "_note_index"] + [x for x in df.columns if "__" in x]

    # Assemble features into a single vector column (required for Spark MLlib)
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    assembled_df = assembler.transform(test_df)

    # Split the dataframe into training subsets (so as not to overfit)
    train_df, test_df = assembled_df.randomSplit([0.65, 0.35], seed=54)

    # Fit the regression model
    lr = LinearRegression(
        featuresCol="features",
        labelCol="_z_rating",
        predictionCol="_predicted_z_rating",
    )
    lr_model = lr.fit(train_df)

    # Apply predictions to the full dataset
    full_assembled = assembler.transform(df)
    predictions_df = lr_model.transform(full_assembled)

    # Select relevant columns
    result_df = predictions_df.select(
        "dbt_id",
        "profile_id",
        "_z_rating",
        "_predicted_z_rating",
        "_note_index",
    )

    return result_df
