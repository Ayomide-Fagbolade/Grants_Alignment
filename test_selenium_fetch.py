import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sys
import os

# Insert scripts directory to the front of sys.path so its local secrets.py takes precedence over stdlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
from browser_session import make_driver



TEST_URLS = [
    "https://allafrica.com/stories/200112310234.html",  # 2001
    "https://allafrica.com/stories/201001050006.html",  # 2010
    "https://allafrica.com/stories/202301100001.html",  # 2023
]

print("Starting headless Chrome...")
driver = make_driver()

try:
    for url in TEST_URLS:
        start = time.time()
        driver.set_page_load_timeout(30)
        driver.get(url)
        elapsed = time.time() - start

        # Extract Publisher_URL & Source_URL via Selenium
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

        headline       = soup.select_one('h2.headline')
        pub_date       = soup.select_one('.publication-date')
        publication    = soup.select_one('.publication')
        body_paragraphs = soup.select('.story-body .story-body-text')

        headline_text    = headline.text.strip()    if headline    else "MISSING"
        pub_date_text    = pub_date.text.strip()    if pub_date    else "MISSING"
        publication_text = publication.text.strip() if publication else "MISSING"
        body_text        = "\n".join([p.text.strip() for p in body_paragraphs])

        print(f"\n{'='*60}")
        print(f"URL:          {url}")
        print(f"Time:         {elapsed:.2f}s")
        print(f"Headline:     {headline_text}")
        print(f"Date:         {pub_date_text}")
        print(f"Publisher:    {publication_text}")
        print(f"Publisher URL:{publisher_url}")
        print(f"Source URL:   {source_url}")
        print(f"Body (chars): {len(body_text)} — {'OK' if body_text else 'MISSING'}")
        print(f"Body snippet: {body_text[:120]}...")

finally:
    driver.quit()
    print("\nDriver closed.")
