import snscrape.modules.twitter as sntwitter

def fetch_twitter_scrape(query="OSINT", limit=10):
    results = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        results.append({
            "platform": "twitter",
            "user": tweet.user.username,
            "timestamp": str(tweet.date),
            "text": tweet.content,
            "url": tweet.url
        })
    return results
