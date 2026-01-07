#!/bin/bash
set -euxo pipefail

# Download vader_lexicon directly from NLTK's GitHub
NLTK_DATA=/opt/conda/default/share/nltk_data
VADER_DIR=$NLTK_DATA/sentiment

mkdir -p $VADER_DIR
cd $VADER_DIR

# Download vader_lexicon.zip directly
wget -q https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/sentiment/vader_lexicon.zip

# Verify download
if [ -f "vader_lexicon.zip" ]; then
    echo "NLTK vader_lexicon downloaded successfully to $VADER_DIR"
    exit 0
else
    echo "ERROR: vader_lexicon download failed"
    exit 1
fi