# utils/visualizer.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_sentiment(db_path="data/osint.db", save_dir="reports"):
    """
    Loads data from the database, plots average sentiment per platform,
    saves chart as PNG, and prints a short summary.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT platform, sentiment FROM osint_data", conn)
    conn.close()

    if df.empty:
        print("⚠️ No data in database to plot.")
        return

    # Group by platform
    avg_sentiment = df.groupby("platform")["sentiment"].mean()

    # --- Plot ---
    plt.figure(figsize=(6, 4))
    avg_sentiment.plot(kind="bar", color=["skyblue", "lightgreen", "salmon"])

    plt.title("Average Sentiment by Platform")
    plt.ylabel("Sentiment Score (-1 = Negative, +1 = Positive)")
    plt.xlabel("Platform")
    plt.xticks(rotation=0)
    plt.ylim(-0.1, 0.3)
    plt.tight_layout()

    # --- Save instead of show ---
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, "sentiment_by_platform.png")
    plt.savefig(save_path)
    plt.close()

    print(f"\n📊 Sentiment chart saved as: {save_path}")

    # --- Analysis ---
    print("\nThe sentiment analysis revealed interesting patterns across platforms:\n")
    for platform, score in avg_sentiment.items():
        if score > 0.1:
            summary = "positive sentiment"
        elif score > 0:
            summary = "slightly positive sentiment"
        elif score < -0.05:
            summary = "negative sentiment"
        else:
            summary = "neutral sentiment"

        print(f"● {platform.capitalize()}: {summary} (approx {score:.2f})")
