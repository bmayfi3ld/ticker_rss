from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import requests
from datetime import datetime, timedelta, timezone
import re
from time import sleep
import os

# Standard Central Time
central_offset = timedelta(hours=-6)
central_time = timezone(central_offset)

# Function to scrape blog page
def scrape_blog(url):
    response = requests.get(url, headers={'User-Agent': 'ticker rss feed generator v0.x'})
    # set a user agent
    soup = BeautifulSoup(response.content, features="lxml")

    # Find the content element
    content_element = soup.find('pre')

    # convert their a tags to img
    a_tags = content_element.find_all('a')

    for a in a_tags:
        img = soup.new_tag('img')

        img['src'] = a['href']
        img['alt'] = a.get_text()
        img['style'] = ' display: block; margin-right: auto; margin-left: auto; width: 100%;' # just some stuff to get it to have its own space

        a.replace_with(img)


    # Extract the content text
    content = content_element.prettify()[36:-20]

    title, date = extract_date_and_title(content_element.get_text(separator="\n"))

    nextEntry = {'content': content, 'title': title, 'date': date, 'link': url}

    print("\n\nfound entry")
    print('title ' + str(nextEntry['title']))
    print('date ' + str(nextEntry['date']))
    print('link ' + nextEntry['link'])
    print('"""')
    print(nextEntry['content'][:100])
    print('"""\n\n')

    return nextEntry

def extract_date_and_title(text):
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

def get_post_urls(base_url):
    # Get today's date
    today = datetime.now()
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

# Function to generate RSS feed
def generate_rss(posts):
    fg = FeedGenerator()
    fg.title('Oklahoma Mesonet Ticker')
    fg.link(href='https://ticker.mesonet.org/', rel='self')
    fg.id('https://ticker.mesonet.org/')
    fg.description('Latest Ticker')
    fg.author({'name': 'Gary McManus', 'email': 'gmcmanus@mesonet.org'})
    fg.copyright('Copyright 2024 Oklahoma Climatological Survey')

    previous_title = ""

    for post in posts:
        if post['title'] == previous_title:
            continue

        fe = fg.add_entry()
        fe.title(post['title'])
        fe.author({'name': 'Gary McManus', 'email': 'gmcmanus@mesonet.org'})
        fe.link(href=post['link'], rel='self')
        fe.content(post['content'], type='html')
        fe.pubDate(post['date'])
        fe.id(post['link'])

        previous_title = post['title']

    folder = os.getenv("RSS_FOLDER")

    if not folder:
        folder = "./"

    fg.atom_file(folder + 'blog_rss.xml')

while True:
    base_url = 'https://ticker.mesonet.org/select.php'
    post_urls = get_post_urls(base_url)

    print("scraping\n" + "\n".join(post_urls))

    all_posts = []
    for url in post_urls:
        posts = scrape_blog(url)

        sleep(3)

        all_posts.append(posts)
    generate_rss(all_posts)

    sleep(3600) # one hour
