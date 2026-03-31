# collectors/hacker_news_collector.py
import requests

def fetch_hn(limit=10):
    """
    Fetch top stories from Hacker News.
    """
    results = []
    try:
        # Get top stories IDs
        top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_ids_url)
        if response.status_code != 200:
            return []
            
        story_ids = response.json()[:limit]

        # Fetch details for each story
        for sid in story_ids:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
            item_res = requests.get(item_url)
            if item_res.status_code == 200:
                item = item_res.json()
                results.append({
                    "platform": "hackernews",
                    "user": item.get("by", "unknown"),
                    "timestamp": str(item.get("time", "")), # Unix timestamp
                    "text": item.get("title", ""),
                    "url": f"https://news.ycombinator.com/item?id={sid}"
                })
    except Exception as e:
        print(f"❌ Error fetching Hacker News: {e}")
        
    return results
