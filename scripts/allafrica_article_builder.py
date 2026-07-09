import csv
import os
import sys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from browser_session import make_driver

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


def build_articles():
    if not os.path.exists(input_csv):
        print(f"Input file not found: {input_csv}")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Resume support: skip already successfully scraped URLs
    processed_urls = load_processed_urls()
    print(f"Found {len(processed_urls)} already successfully processed articles.")

    with open(input_csv, 'r', encoding='utf-8') as f:
        all_rows = list(csv.DictReader(f))

    rows_to_process = [r for r in all_rows if r['Link'] not in processed_urls]
    total = len(rows_to_process)
    print(f"Articles left to process: {total}")

    if not rows_to_process:
        print("Everything is processed!")
        return

    print("Setting up authenticated headless Chrome...")
    driver = make_driver()

    open_files: dict = {}
    writers: dict = {}

    try:
        for count, row in enumerate(rows_to_process, 1):
            url = row['Link']
            year = get_year_from_url(url) or 'unknown'
            print(f"[{count}/{total}] [{year}] {url}")

            try:
                driver.set_page_load_timeout(30)
                driver.get(url)

                try:
                    source_el = driver.find_element(By.CSS_SELECTOR, 'a.source-url')
                    source_url = source_el.get_attribute('href')
                except Exception:
                    source_url = "N/A"

                try:
                    publisher_el = driver.find_element(By.CSS_SELECTOR, 'a.publisher-url')
                    publisher_url = publisher_el.get_attribute('href')
                except Exception:
                    publisher_url = "N/A"

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                headline = soup.select_one('h2.headline')
                headline_text = headline.text.strip() if headline else "N/A"

                pub_date = soup.select_one('.publication-date')
                pub_date_text = pub_date.text.strip() if pub_date else "N/A"

                publication = soup.select_one('.publication')
                publication_text = publication.text.strip() if publication else "N/A"

                body_paragraphs = soup.select('.story-body .story-body-text')
                body_text = "\n".join([p.text.strip() for p in body_paragraphs])

                # Only write if we got meaningful content
                if headline_text != 'N/A' and body_text:
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
                    print(f"  Skipped (no content): {url}")

            except Exception as e:
                print(f"  [ERROR] {url} — {e}")
                # Not written, will be retried next run

    finally:
        for f in open_files.values():
            f.close()
        driver.quit()
        print("Done. Driver closed.")


if __name__ == "__main__":
    build_articles()
