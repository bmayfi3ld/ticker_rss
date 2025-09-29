#!/usr/bin/env python3
"""
Test script to simulate scraping for specific dates around September 27-28, 2025,
to check if the article 'Chilly' (assumed to be from August 29, 2025) drops off and pops up again.
"""

import os
import sys
from datetime import datetime, date
from typing import List

# Add the current directory to sys.path to import from main.py
sys.path.insert(0, os.path.dirname(__file__))

from main import get_post_urls, scrape_blog, generate_rss

# Assume 'Chilly' is from August 29, 2025
CHILLY_DATE = date(2025, 8, 29)
CHILLY_TITLE = "Chilly"


def test_for_date(test_date: date, ticker_days: int = 30) -> List[str]:
    """
    Simulate getting post URLs for a specific date and check if 'Chilly' URL is included.
    """
    base_url = "https://ticker.mesonet.org/select.php"

    # Set environment variable for TICKER_DAYS
    os.environ["TICKER_DAYS"] = str(ticker_days)

    urls = get_post_urls(base_url, today=test_date)

    chilly_url = None
    for url in urls:
        # Parse the date from URL
        # URL format: ?mo=08&da=29&yr=2025
        if "mo=08&da=29&yr=2025" in url:
            chilly_url = url
            break

    print(f"For date {test_date}, TICKER_DAYS={ticker_days}:")
    print(f"  URLs generated: {len(urls)}")
    print(f"  Chilly URL included: {chilly_url is not None}")
    if chilly_url:
        print(f"  Chilly URL: {chilly_url}")

    # Simulate scraping (will return None for future dates)
    posts = []
    for url in urls:
        post = scrape_blog(url)
        if post and post["title"] == CHILLY_TITLE:
            posts.append(post)

    print(f"  Posts found: {len(posts)}")
    for post in posts:
        print(f"    Title: {post['title']}, Date: {post['date']}")

    return urls


def main():
    # Test for September 27, 2025
    test_for_date(date(2025, 9, 27), ticker_days=30)
    print()

    # Test for September 28, 2025
    test_for_date(date(2025, 9, 28), ticker_days=30)
    print()

    # Test with TICKER_DAYS=31 to see if it includes Chilly on Sep 28
    test_for_date(date(2025, 9, 28), ticker_days=31)


if __name__ == "__main__":
    main()
