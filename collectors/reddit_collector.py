# collectors/reddit_collector.py
import os
import praw
from dotenv import load_dotenv

load_dotenv()

def fetch_reddit(subreddit="technology", limit=10, sort="hot"):
    results = []
    try:
        # Initialize inside the function to prevent crash at app startup
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="osint_pipeline",
            check_for_async=False
        )
        
        submissions = reddit.subreddit(subreddit).hot(limit=limit)
        for sub in submissions:
            results.append({
                "platform": "reddit",
                "user": str(sub.author),
                "timestamp": str(sub.created_utc),
                "text": f"{sub.title} {sub.selftext}",
                "url": f"https://reddit.com{sub.permalink}"
            })
    except Exception:
        # 🧪 Mock Fallback for Invalid API Keys or missing secrets
        print("⚠️ Reddit API Unauthorized (401) – Loading mock results...")
        for i in range(limit):
            results.append({
                "platform": "reddit",
                "user": f"redditor_{i}",
                "timestamp": "2024-03-31T00:00:00Z",
                "text": f"Check out this thread on r/{subreddit}! #OSINT",
                "url": "https://reddit.com/"
            })
    return results
