from bs4 import BeautifulSoup, Tag
from feedgen.feed import FeedGenerator
import requests
from datetime import datetime, timedelta, timezone
import re
from time import sleep
import os
from typing import Optional, Dict, Any
import threading
from flask import Flask, send_file, jsonify
import logging
from waitress import serve

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Standard Central Time
central_offset = timedelta(hours=-6)
central_time = timezone(central_offset)

# Flask app
app = Flask(__name__)

# Function to scrape blog page
def scrape_blog(url: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(url, headers={'User-Agent': 'ticker rss feed generator v0.x'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features="lxml")

        # Find the content element
        content_element = soup.find('pre')

        if content_element is None or not isinstance(content_element, Tag):
            return None

        # convert their a tags to img
        a_tags = content_element.find_all('a')

        for a in a_tags:
            if isinstance(a, Tag):
                img = soup.new_tag('img')

                href = a.get('href')
                if href:
                    img['src'] = href
                img['alt'] = a.get_text()
                img['style'] = ' display: block; margin-right: auto; margin-left: auto; width: 100%;'

                a.replace_with(img)

        # Extract the content text
        content = content_element.prettify()[36:-20]

        title, date = extract_date_and_title(content_element.get_text(separator="\n"))

        nextEntry = {'content': content, 'title': title, 'date': date, 'link': url}

        logger.info(f"Found entry: {title} - {date}")
        return nextEntry

    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return None

def extract_date_and_title(text: str) -> tuple[Optional[str], Optional[datetime]]:
    # Regex pattern to match the date and title
    pattern = r'MESONET TICKER \.\.\. MESONET TICKER \.\.\. MESONET TICKER \.\.\. MESONET TICKER \.\.\.\n(?P<date>\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4})[^\n]*\n(?P<title>[^\n]*)\n'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        title = match.group('title').strip()
        date_str = match.group('date').strip()
        # Parse the date string into a datetime object
        date = datetime.strptime(date_str, '%B %d, %Y')

        # Attach the Central Time timezone information to the naive datetime object
        central_date = date.replace(tzinfo=central_time)

        return title, central_date
    else:
        return None, None

def get_post_urls(base_url: str) -> list[str]:
    # Get today's date in Central Time
    today = datetime.now(central_time)
    urls = []
    # Loop over the last days
    days = os.getenv("TICKER_DAYS")

    if not days:
        days = 30

    for i in range(int(days)):
        # Calculate the date for each day
        date = today - timedelta(days=i)
        # Construct the URL for the post using the date
        url = f"{base_url}?mo={date.strftime('%m')}&da={date.strftime('%d')}&yr={date.strftime('%Y')}"
        urls.append(url)

    urls.reverse()
    return urls

def get_rss_file_path() -> str:
    folder = os.getenv("RSS_FOLDER", "./")
    if not folder.endswith('/'):
        folder += '/'
    return folder + 'blog_rss.xml'

# Function to generate RSS feed
def generate_rss(posts: list[Dict[str, Any]]) -> None:
    try:
        fg = FeedGenerator()
        fg.title('Oklahoma Mesonet Ticker')
        fg.link(href='https://ticker.mesonet.org/', rel='self')
        fg.id('https://ticker.mesonet.org/')
        fg.description('Latest Ticker')
        fg.author({'name': 'Gary McManus', 'email': 'gmcmanus@mesonet.org'})
        fg.copyright('Copyright 2024 Oklahoma Climatological Survey')

        previous_title = ""
        valid_entries = 0

        for post in posts:
            if post['title'] == previous_title or not post['title']:
                continue

            fe = fg.add_entry()
            fe.title(post['title'])
            fe.author({'name': 'Gary McManus', 'email': 'gmcmanus@mesonet.org'})
            fe.link(href=post['link'], rel='self')
            fe.content(post['content'], type='html')
            fe.pubDate(post['date'])
            fe.id(post['link'])

            previous_title = post['title']
            valid_entries += 1

        rss_file_path = get_rss_file_path()
        fg.atom_file(rss_file_path)

        logger.info(f"RSS feed generated with {valid_entries} entries at {rss_file_path}")

    except Exception as e:
        logger.error(f"Error generating RSS feed: {e}")

def scraper_worker():
    """Background worker that continuously scrapes and generates RSS feeds"""
    logger.info("Starting RSS scraper worker...")

    while True:
        try:
            base_url = 'https://ticker.mesonet.org/select.php'
            post_urls = get_post_urls(base_url)

            logger.info(f"Scraping {len(post_urls)} URLs...")

            all_posts = []
            for url in post_urls:
                posts = scrape_blog(url)
                sleep(3)  # Rate limiting

                if posts is not None:
                    all_posts.append(posts)

            logger.info(f"Found {len(all_posts)} valid posts")
            generate_rss(all_posts)

            logger.info("Sleeping for 1 hour until next scrape...")
            sleep(3600)  # one hour

        except Exception as e:
            logger.error(f"Error in scraper worker: {e}")
            sleep(300)  # Sleep 5 minutes on error before retrying

# Flask routes
@app.route('/')
def index():
    """Simple index page"""
    rss_file_path = get_rss_file_path()
    file_exists = os.path.exists(rss_file_path)

    if file_exists:
        return '''
        <h1>Oklahoma Mesonet Ticker RSS</h1>
        <p>RSS feed is available at: <a href="/rss">/rss</a></p>
        <p>Status: <a href="/status">/status</a></p>
        '''
    else:
        return '''
        <h1>Oklahoma Mesonet Ticker RSS</h1>
        <p>RSS feed is being generated, please wait...</p>
        <p>Status: <a href="/status">/status</a></p>
        '''

@app.route('/rss')
def serve_rss():
    """Serve the RSS feed file from disk"""
    rss_file_path = get_rss_file_path()

    if not os.path.exists(rss_file_path):
        return jsonify({
            'error': 'RSS feed not yet generated',
            'message': 'Please wait for the initial feed generation'
        }), 404

    return send_file(rss_file_path, mimetype='application/rss+xml')

@app.route('/status')
def status():
    """API endpoint for RSS feed status"""
    rss_file_path = get_rss_file_path()
    file_exists = os.path.exists(rss_file_path)

    status_info = {
        'file_exists': file_exists,
        'rss_file_path': rss_file_path,
        'ticker_days': int(os.getenv('TICKER_DAYS', 30))
    }

    if file_exists:
        try:
            file_stat = os.stat(rss_file_path)
            status_info['file_size'] = file_stat.st_size
            status_info['file_modified'] = datetime.fromtimestamp(file_stat.st_mtime, tz=central_time).isoformat()
        except Exception as e:
            logger.error(f"Error getting file stats: {e}")

    return jsonify(status_info)

if __name__ == '__main__':
    import sys

    # Check if Flask should be disabled (scraper-only mode)
    disable_flask = os.getenv('DISABLE_FLASK', 'false').lower() == 'true'

    if disable_flask:
        logger.info("Running in scraper-only mode (Flask disabled)")
        try:
            scraper_worker()  # Run scraper directly
        except KeyboardInterrupt:
            logger.info("Scraper stopped by user")
            sys.exit(0)
    else:
        # Start the scraper in a background thread
        scraper_thread = threading.Thread(target=scraper_worker, daemon=True)
        scraper_thread.start()

        # Get server configuration from environment
        host = os.getenv('FLASK_HOST', '0.0.0.0')
        port = int(os.getenv('FLASK_PORT', 5000))
        threads = int(os.getenv('WAITRESS_THREADS', 4))
        connection_limit = int(os.getenv('WAITRESS_CONNECTION_LIMIT', 1000))
        cleanup_interval = int(os.getenv('WAITRESS_CLEANUP_INTERVAL', 30))
        channel_timeout = int(os.getenv('WAITRESS_CHANNEL_TIMEOUT', 120))

        logger.info(f"Starting Waitress server on {host}:{port}")
        logger.info(f"Server config: {threads} threads, {connection_limit} connection limit")
        logger.info(f"RSS feed will be available at http://{host}:{port}/rss")

        try:
            serve(app,
                  host=host,
                  port=port,
                  threads=threads,
                  connection_limit=connection_limit,
                  cleanup_interval=cleanup_interval,
                  channel_timeout=channel_timeout)
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
            sys.exit(0)
