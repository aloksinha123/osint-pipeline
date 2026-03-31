# collectors/twitter_collector.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TWITTER_BEARER = os.getenv("TWITTER_BEARER")

def fetch_twitter(query="OSINT", limit=10):
    results = []
    try:
        url = "https://api.twitter.com/2/users/by/username/TwitterDev"
        headers = {"Authorization": f"Bearer {TWITTER_BEARER}"}
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            data = res.json().get("data", {})
            results.append({
                "platform": "twitter",
                "user": "TwitterDev",
                "timestamp": "2024-03-31T00:00:00Z",
                "text": data.get("description", ""),
                "url": "https://twitter.com/TwitterDev"
            })
        else:
            raise Exception("Twitter API limited")
            
    except Exception:
        # 🧪 Mock Fallback for Free Tier
        print("⚠️ Twitter Search API limited (Free Tier) – Loading mock results...")
        for i in range(limit):
            results.append({
                "platform": "twitter",
                "user": f"user_{i}",
                "timestamp": "2024-03-31T00:00:00Z",
                "text": f"Discussing latest #OSINT techniques and tools! Search query: {query}",
                "url": "https://twitter.com/"
            })
    return results
