"""
This model performs semantic analysis on whiskey tasting notes
using selected features from the staging feature selection model.
"""

import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

#####


# Ensure NLTK data is downloaded (needs to run on each worker)
def _ensure_vader_lexicon():

    # Use /tmp as download directory (always writable)
    download_dir = "/tmp/nltk_data"

    # Add to NLTK data path if not already present
    if download_dir not in nltk.data.path:
        nltk.data.path.insert(0, download_dir)

    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        # Ensure directory exists
        os.makedirs(download_dir, exist_ok=True)
        nltk.download("vader_lexicon", download_dir=download_dir, quiet=True)


def analyze_sentiment(text: str) -> dict:
    """
    Determines if a string is positive, negative, or neutral.
    Returns a dictionary with the label and the raw score.
    """
    # Download on each worker if needed
    _ensure_vader_lexicon()

    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)

    # The 'compound' score ranges from -1 (most neg) to 1 (most pos)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"

    elif compound <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return {"label": sentiment, "score": compound}


def analyze_text(df: pd.DataFrame) -> None:
    """
    Placeholder function for semantic analysis.
    In a real implementation, this would involve NLP techniques
    to extract meaningful features from the tasting notes.
    """

    df["review_sentiment"] = df["review"].apply(lambda x: analyze_sentiment(x)["label"])
    df["semantic_score"] = df["review"].apply(lambda x: analyze_sentiment(x)["score"])


def model(dbt, session) -> pd.DataFrame:
    df = dbt.ref("stg__setup").toPandas()

    df = df.loc[:, ["dbt_id", "review"]]

    # Ensure VADER lexicon is available
    _ensure_vader_lexicon()

    analyze_text(df=df)

    return df.loc[:, ["dbt_id", "review_sentiment", "semantic_score"]]
