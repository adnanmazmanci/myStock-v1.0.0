import feedparser
import hashlib
import os
from datetime import datetime
from utils.headline_tagger import tag_headline
import requests
import email.utils
import time
import random

SEEN_HEADLINES_PATH = "data/seen_headlines.txt"
MAX_HEADLINES = 20

FEEDS = {
    "Breaking News": "https://www.investing.com/rss/news_301.rss",
    "Stock Market": "https://www.investing.com/rss/news_25.rss",
    "Stock": "https://www.investing.com/rss/news_1061.rss",
    "Stock Market Investment Ideas": "https://www.investing.com/rss/news_1065.rss",
    "Forex": "https://www.investing.com/rss/news_1.rss",
    "Cryptocurrency": "https://www.investing.com/rss/news_301.rss",
    "Earnings Reports and Whispers": "https://www.investing.com/rss/news_1062.rss",
    "Insider Trading News": "https://www.investing.com/rss/news_357.rss"
}

def load_seen():
    if not os.path.exists(SEEN_HEADLINES_PATH):
        return set()
    with open(SEEN_HEADLINES_PATH, "r") as f:
        return set(line.strip() for line in f)

def save_seen(seen):
    with open(SEEN_HEADLINES_PATH, "w") as f:
        for h in seen:
            f.write(h + "\n")

def hash_headline(title):
    return hashlib.sha1(title.encode()).hexdigest()

def fetch_with_retry(url, retries=3, initial_delay=5):
    """Fetch the URL with retry, exponential backoff, and random delay"""
    attempt = 0
    delay = initial_delay  # Start with a small delay

    while attempt < retries:
        try:
            # Print the feed being processed
            print(f"🔄 Attempting to fetch {url}...")

            # Add a random delay between requests to avoid being throttled
            time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds

            # Set a custom User-Agent to mimic regular browser traffic
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

            # Fetch the RSS feed with a 60-second timeout
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()  # Raise exception for bad status codes
            return response  # Return the successful response

        except requests.Timeout as e:
            error_message = f"⚠️ Timeout occurred while fetching {url}. Retrying in {delay} seconds..."
            print(error_message)
            print(f"Error details: {e}")  # Print the specific timeout error details
            time.sleep(delay)  # Exponentially increase the delay after each retry
            attempt += 1
            delay *= 2  # Exponentially increase the delay (e.g., 5s, 10s, 20s)

        except requests.RequestException as e:
            error_message = f"⚠️ Error fetching {url}: {e}"
            print(error_message)
            print(f"Error details: {e}")  # Print the specific error details
            break  # Exit the loop if it's a non-timeout error

    print(f"❌ Failed to fetch {url} after {retries} retries.")
    return None  # Return None if all retries fail

def collect_latest_headlines():
    seen = load_seen()
    new_seen = set()
    all_items = []

    for source, url in FEEDS.items():
        print(f"🔍 Fetching headlines from: {source}")  # Print the source name being fetched

        response = fetch_with_retry(url)
        if not response:
            continue  # Skip this feed if all retries fail

        feed = feedparser.parse(response.content)

        for entry in feed.entries:
            title = entry.title.strip()
            link = entry.link.strip()
            pub_date = entry.get("published", "")
            tag = tag_headline(title)
            h_hash = hash_headline(title)

            if h_hash not in seen:
                all_items.append({
                    "title": title,
                    "link": link,
                    "timestamp": pub_date,
                    "tag": tag,
                    "source": source,
                    "hash": h_hash
                })
                new_seen.add(h_hash)

    # Sort by latest date if available
    all_items = sorted(all_items, key=lambda x: x['timestamp'], reverse=True)
    top_items = all_items[:MAX_HEADLINES]

    save_seen(seen.union(new_seen))

    return top_items
