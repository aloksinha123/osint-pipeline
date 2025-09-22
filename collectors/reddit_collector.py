# collectors/reddit_collector.py
import os
from dotenv import load_dotenv
import praw
from datetime import datetime

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "osint_pipeline")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    check_for_async=False
)

def fetch_reddit(subreddit="technology", limit=10, sort="hot"):
    """
    Fetch posts from a subreddit.
    """
    results = []
    try:
        if sort == "hot":
            submissions = reddit.subreddit(subreddit).hot(limit=limit)
        elif sort == "new":
            submissions = reddit.subreddit(subreddit).new(limit=limit)
        elif sort == "top":
            submissions = reddit.subreddit(subreddit).top(limit=limit)
        else:
            submissions = reddit.subreddit(subreddit).hot(limit=limit)

        for sub in submissions:
            author = str(sub.author) if sub.author else "deleted"
            text = (sub.title or "") + " " + (sub.selftext or "")
            timestamp = datetime.utcfromtimestamp(sub.created_utc).isoformat() + "Z"
            url = f"https://reddit.com{sub.permalink}"

            results.append({
                "platform": "reddit",
                "user": author,
                "timestamp": timestamp,
                "text": text,
                "url": url
            })
    except Exception as e:
        print(f"❌ Error fetching reddit posts: {e}")
    return results
