import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
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

    # Initialize NLTK on the worker
    nltk.download("vader_lexicon", quiet=True)
    nltk.data.path.append("/opt/conda/default/share/nltk_data")
    sia = SentimentIntensityAnalyzer()

    results = []
    for text in reviews:
        # Handle nulls
        if text is None or text == "":
            results.append({"review_sentiment": "Neutral", "semantic_score": 0.0})
            continue

        scores = sia.polarity_scores(str(text))
        compound = scores["compound"]

        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        results.append({"review_sentiment": sentiment, "semantic_score": compound})

    return pd.DataFrame(results)


def model(dbt, session):
    # dbt settings
    dbt.config(materialized="table")

    # 2. Use Spark DataFrame instead of .toPandas()
    # This stays on the cluster and does not pull data to the master node
    df = dbt.ref("stg__setup").select("dbt_id", "review")

    # 3. Apply the UDF
    # This creates a new 'struct' column containing both label and score
    df_result = df.withColumn("sentiment_results", get_sentiment_spark(df["review"]))

    # 4. Flatten the results and return
    return df_result.select(
        "dbt_id",
        "sentiment_results.review_sentiment",
        "sentiment_results.semantic_score",
    )
