import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pyspark import SparkFiles
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import DoubleType, StringType, StructField, StructType

#####

result_schema = StructType(
    [
        StructField("review_sentiment", StringType(), True),
        StructField("semantic_score", DoubleType(), True),
    ]
)


@pandas_udf(result_schema)
def get_sentiment_spark(reviews: pd.Series) -> pd.DataFrame:
    """
    This function runs on the WORKER nodes in parallel.
    It receives a Pandas Series of reviews and must return a Pandas DataFrame
    matching the result_schema.
    """

    local_path = SparkFiles.get("vader_lexicon.txt")

    # Initialize NLTK on the worker
    sia = SentimentIntensityAnalyzer(lexicon_file=local_path)

    results = []
    for text in reviews:
        # Handle nulls
        if text is None or text == "":
            results.append({"review_sentiment": "Neutral", "semantic_score": 0.0})
            continue

        scores = sia.polarity_scores(str(text))
        compound = scores["compound"]

        # NOTE: Kind of a naive threshold but good enough for now
        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        results.append({"review_sentiment": sentiment, "semantic_score": compound})

    return pd.DataFrame(results)


def model(dbt, session):
    # Pull in the staging data with the relevant columns
    df = dbt.ref("stg__setup").select("dbt_id", "review")

    gcs_lexicon_path = "gs://whiskey-ml-dataproc-staging-bucket/vader_lexicon.txt"
    session.sparkContext.addFile(gcs_lexicon_path)

    # This creates a new 'struct' column containing both label and score
    df_result = df.withColumn("sentiment_results", get_sentiment_spark(df["review"]))

    return df_result.select(
        "dbt_id",
        "sentiment_results.review_sentiment",
        "sentiment_results.semantic_score",
    )
