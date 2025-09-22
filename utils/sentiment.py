# utils/sentiment.py
from textblob import TextBlob

def add_sentiment(records):
    for r in records:
        if "text" in r and isinstance(r["text"], str):
            try:
                r["sentiment"] = TextBlob(r["text"]).sentiment.polarity
            except Exception:
                r["sentiment"] = 0.0
        else:
            r["sentiment"] = 0.0
    return records
