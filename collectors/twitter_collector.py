# collectors/twitter_collector.py
import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Load Bearer Token from .env
TWITTER_BEARER = os.getenv("TWITTER_BEARER")

# Initialize Tweepy Client (v2)
client = tweepy.Client(bearer_token=TWITTER_BEARER)

def fetch_twitter(query="OSINT", limit=10):
    """
    Fetch tweets using Twitter API v2 (requires Bearer Token).
    """
    results = []
    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=min(limit, 100),  # API allows max 100 per request
            tweet_fields=["created_at", "text", "author_id"]
        )
        if tweets.data:
            for t in tweets.data:
                results.append({
                    "platform": "twitter",
                    "user": t.author_id,
                    "timestamp": str(t.created_at),
                    "text": t.text,
                    "url": f"https://twitter.com/i/web/status/{t.id}"
                })
    except Exception as e:
        print(f"❌ Error fetching tweets: {e}")
    return results
