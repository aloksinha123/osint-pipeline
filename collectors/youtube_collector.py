# collectors/youtube_collector.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_youtube(query="OSINT cybersecurity", limit=10):
    """
    Fetch videos from YouTube search API.
    """
    try:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            print("⚠️ No YouTube API Key found in .env")
            return []

        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": min(limit, 50),
            "key": api_key
        }

        res = requests.get(url, params=params)
        data = res.json()

        videos = []
        for item in data.get("items", []):
            snippet = item["snippet"]
            videos.append({
                "platform": "youtube",
                "user": snippet.get("channelTitle", "unknown"),
                "timestamp": snippet.get("publishedAt", ""),
                "text": snippet.get("title", ""),
                "url": f"https://www.youtube.com/watch?v={item.get('id', {}).get('videoId', '')}"
            })

        return videos

    except Exception as e:
        print("❌ YouTube error:", e)
        return []
