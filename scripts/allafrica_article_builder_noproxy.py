import csv
import os
import sys
import requests
import urllib.parse
import importlib.util
from bs4 import BeautifulSoup
import urllib3
import time
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

input_csv = r'c:\Users\ayo\Desktop\Grants_Alignment\media_data\allafrica_results_unique.csv'
output_dir = r'c:\Users\ayo\Desktop\Grants_Alignment\media_data\articles_by_year'

FIELDNAMES = ['Crops', 'Original_Search_Title', 'Link', 'Headline', 'Date',
              'Publisher', 'Publisher_URL', 'Source_URL', 'Body_Text']


def get_year_from_url(url: str) -> str | None:
    """Extract 4-digit year from allafrica URL e.g. /stories/202507..."""
    try:
        year = url.split('/stories/')[1][:4]
        if year.isdigit():
            return year
    except (IndexError, ValueError):
        pass
    return None


def load_processed_urls() -> set:
    """Scan all existing year CSVs and return the set of already-scraped URLs."""
    csv.field_size_limit(sys.maxsize)
    processed = set()
    if not os.path.exists(output_dir):
        return processed
    for fname in os.listdir(output_dir):
        if fname.endswith('.csv'):
            fpath = os.path.join(output_dir, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        url = row.get('Link', '').strip()
                        body = row.get('Body_Text', '').strip()
                        headline = row.get('Headline', 'N/A').strip()
                        # Only count as processed if the scrape actually succeeded
                        if url and body and headline != 'N/A':
                            processed.add(url)
            except Exception:
                pass
    return processed


def get_year_writer(year: str, open_files: dict, writers: dict):
    """Return (file, writer) for the given year, opening a new one if needed."""
    if year not in writers:
        fpath = os.path.join(output_dir, f'allafrica_{year}.csv')
        file_exists = os.path.exists(fpath)
        f = open(fpath, mode='a', newline='', encoding='utf-8')
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists or os.stat(fpath).st_size == 0:
            writer.writeheader()
        open_files[year] = f
        writers[year] = writer
    return open_files[year], writers[year]


def build_articles(target_years: list = None):
    if not os.path.exists(input_csv):
        print(f"Input file not found: {input_csv}")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Resume support: skip already successfully scraped URLs
    processed_urls = load_processed_urls()
    print(f"Found {len(processed_urls)} already successfully processed articles.")

    with open(input_csv, 'r', encoding='utf-8') as f:
        all_rows = list(csv.DictReader(f))

    rows_to_process = []
    for r in all_rows:
        if r['Link'] not in processed_urls:
            year = get_year_from_url(r['Link'])
            if target_years:
                if year in target_years:
                    rows_to_process.append(r)
            else:
                rows_to_process.append(r)

    total = len(rows_to_process)
    if target_years:
        print(f"Articles left to process for {', '.join(target_years)}: {total}")
    else:
        print(f"Articles left to process: {total}")

    if not rows_to_process:
        print("Everything is processed for this selection!")
        return

    print("Setting up requests Session with proxy cookies...")
    
    # Load secrets.py directly to avoid clash with stdlib 'secrets' module
    _spec = importlib.util.spec_from_file_location(
        "allafrica_secrets",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "secrets.py")
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

    session = requests.Session()
    session.cookies.update(parse_cookies(ALLAFRICA_COOKIES))
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://allafrica.com/search/advanced.html",
    })

    open_files: dict = {}
    writers: dict = {}

    try:
        for count, row in enumerate(rows_to_process, 1):
            url = row['Link']
            year = get_year_from_url(url) or 'unknown'
            print(f"[{count}/{total}] [{year}] {url}")
            time.sleep(random.uniform(1, 3))

            try:
                r = session.get(url, timeout=15, verify=True)
                soup = BeautifulSoup(r.text, 'html.parser')

                source_el = soup.select_one('a.source-url')
                source_url = source_el.get('href') if source_el else "N/A"

                publisher_el = soup.select_one('a.publisher-url')
                publisher_url = publisher_el.get('href') if publisher_el else "N/A"

                headline = soup.select_one('h2.headline')
                headline_text = headline.text.strip() if headline else "N/A"

                pub_date = soup.select_one('.publication-date')
                pub_date_text = pub_date.text.strip() if pub_date else "N/A"

                publication = soup.select_one('.publication')
                publication_text = publication.text.strip() if publication else "N/A"

                body_paragraphs = soup.select('.story-body .story-body-text')
                body_text = "\n".join([p.text.strip() for p in body_paragraphs])

                # Fallback for publisher URL if main tag missing (common in older articles)
                if publisher_url == "N/A":
                    pub_a = soup.select_one('.publication a')
                    if pub_a:
                        publisher_url = pub_a.get('href') or "N/A"

                # Only write if we got meaningful content (headline and body)
                if headline_text != 'N/A' and body_text:
                    # Warn on any N/A fields
                    if source_url == 'N/A':
                        print(f"  [N/A] Source_URL missing:    {url}")
                    if publisher_url == 'N/A':
                        print(f"  [N/A] Publisher_URL missing: {url}")
                    if pub_date_text == 'N/A':
                        print(f"  [N/A] Date missing:          {url}")
                    if publication_text == 'N/A':
                        print(f"  [N/A] Publisher missing:     {url}")

                    _, writer = get_year_writer(year, open_files, writers)
                    writer.writerow({
                        'Crops': row.get('Crops', 'N/A'),
                        'Original_Search_Title': row.get('Title', 'N/A'),
                        'Link': url,
                        'Headline': headline_text,
                        'Date': pub_date_text,
                        'Publisher': publication_text,
                        'Publisher_URL': publisher_url,
                        'Source_URL': source_url,
                        'Body_Text': body_text
                    })
                    open_files[year].flush()
                else:
                    print(f"  [SKIP] No content: {url}")

            except Exception as e:
                print(f"  [ERROR] {url} — {e}")
                # Not written, will be retried next run

    finally:
        for f in open_files.values():
            f.close()
        session.close()
        print("Done. Session closed.")


if __name__ == "__main__":
    targets = None
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    build_articles(targets)
