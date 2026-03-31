from collectors.twitter_collector import fetch_twitter
from collectors.reddit_collector import fetch_reddit
from collectors.github_collector import fetch_github
from collectors.hacker_news_collector import fetch_hn
from collectors.youtube_collector import fetch_youtube

from utils.cleaner import clean_text, filter_english
from utils.database import save_to_db, load_from_db
from utils.sentiment import add_sentiment
from utils.visualizer import plot_sentiment

def run_pipeline():
    data = []

    print("🧹 Cleaning text...")
    # Collect
    twitter_records = fetch_twitter("OSINT", 10)
    reddit_records = fetch_reddit("technology", 10, sort="hot")
    github_records = fetch_github("osint", 10)
    hn_records = fetch_hn(10)
    yt_records = fetch_youtube("OSINT cybersecurity", 10)
    
    data.extend(twitter_records + reddit_records + github_records + hn_records + yt_records)

    # Clean
    for d in data:
        d["text"] = clean_text(d.get("text", ""))
    data = filter_english(data)

    print("🤔 Adding sentiment...")
    # Sentiment
    data = add_sentiment(data)

    print("💾 Saving to database...")
    # Save
    save_to_db(data)

    total = len(data)
    print(f"✅ Pipeline finished. Collected {total} records from Twitter, Reddit, and GitHub\n")

    # Show sample results (first 5)
    print("📊 Sample results:\n")
    for i, r in enumerate(data[:5], start=1):
        platform = r['platform']
        user = r['user']
        sentiment = f"{r['sentiment']:.2f}"
        text = r['text'][:70] + "..." if len(r['text']) > 70 else r['text']
        print(f"{i}. {platform:<7} | {user:<15} | {sentiment:<5} | {text}")

    # Show DB count
    db_records = load_from_db()
    print(f"\n📦 Database now contains {len(db_records)} total records.\n")

    # Plot
    plot_sentiment()

if __name__ == "__main__":
    run_pipeline()
