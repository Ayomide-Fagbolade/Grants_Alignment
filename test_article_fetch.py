import requests
import urllib.parse
import time
import sys
import os
import importlib.util
from bs4 import BeautifulSoup

# Load secrets.py directly to avoid clash with stdlib 'secrets' module
_spec = importlib.util.spec_from_file_location(
    "allafrica_secrets",
    r"c:\Users\ayo\Desktop\Grants_Alignment\scripts\secrets.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
ALLAFRICA_COOKIES = _mod.ALLAFRICA_COOKIES


def parse_cookies(raw: str) -> dict:
    cookies = {}
    for part in raw.split('; '):
        part = part.strip()
        if '=' in part:
            n, _, v = part.partition('=')
            cookies[n.strip()] = urllib.parse.unquote(v)
    return cookies

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://allafrica.com/",
}

COOKIES = parse_cookies(ALLAFRICA_COOKIES)

# A few test URLs from different years
TEST_URLS = [
    "https://allafrica.com/stories/200112310234.html",  # 2001
    "https://allafrica.com/stories/201001050006.html",  # 2010
    "https://allafrica.com/stories/202301100001.html",  # 2023
]

session = requests.Session()
session.cookies.update(COOKIES)
session.headers.update(HEADERS)

for url in TEST_URLS:
    start = time.time()
    
    r = session.get(url, timeout=15)
    elapsed = time.time() - start
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Extract all required columns
    headline = soup.select_one('h2.headline')
    pub_date = soup.select_one('.publication-date')
    publication = soup.select_one('.publication')
    body_paragraphs = soup.select('.story-body .story-body-text')
    source_tag = soup.select_one('a.source-url')
    publisher_url_tag = soup.select_one('a.publisher-url')
    
    headline_text     = headline.text.strip()         if headline         else "MISSING"
    pub_date_text     = pub_date.text.strip()         if pub_date         else "MISSING"
    publication_text  = publication.text.strip()      if publication      else "MISSING"
    body_text         = "\n".join([p.text.strip() for p in body_paragraphs])
    source_url        = source_tag.get('href')        if source_tag       else "N/A"
    publisher_url     = publisher_url_tag.get('href') if publisher_url_tag else "N/A"

    print(f"\n{'='*60}")
    print(f"URL:          {url}")
    print(f"HTTP Status:  {r.status_code}")
    print(f"Time:         {elapsed:.2f}s")
    print(f"Headline:     {headline_text}")
    print(f"Date:         {pub_date_text}")
    print(f"Publisher:    {publication_text}")
    print(f"Publisher URL:{publisher_url}")
    print(f"Source URL:   {source_url}")
    print(f"Body (chars): {len(body_text)} — {'OK' if body_text else 'MISSING'}")
    print(f"Body snippet: {body_text[:120]}...")
