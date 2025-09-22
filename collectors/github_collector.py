# collectors/github_collector.py
import os
from github import Github
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_github(query="osint", limit=10):
    """
    Fetch repositories from GitHub using a search query.
    If GITHUB_TOKEN is missing, falls back to unauthenticated access (low rate limits).
    """
    results = []
    try:
        if GITHUB_TOKEN:
            g = Github(GITHUB_TOKEN)
        else:
            print("⚠️ No GitHub token found in .env, using unauthenticated access (very limited).")
            g = Github()

        repos = g.search_repositories(query=query, sort="stars", order="desc")

        for i, repo in enumerate(repos):
            if i >= limit:
                break
            results.append({
                "platform": "github",
                "user": repo.owner.login,
                "timestamp": str(repo.created_at),
                "text": repo.description or "",
                "url": repo.html_url
            })

    except Exception as e:
        print(f"❌ Error fetching GitHub repos: {e}")

    return results
