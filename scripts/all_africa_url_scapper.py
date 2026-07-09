import time
import urllib.parse
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from crop_list_and_cat_file import crops_list

def check_allafrica():
    results = []
    
    # Set up headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        for crop in crops_list:
            search_term = urllib.parse.quote_plus(crop) 
            url = f"https://allafrica.com/search/?search_string={search_term}&search_submit=Search"
            
            print(f"Searching allafrica.com for '{crop}'...")
            driver.get(url)
            
            # Wait for the results div to appear (max 15 seconds)
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results"))
                )
                print(f"Successfully loaded search results for '{crop}'")
            except Exception as e:
                print(f"Warning: Search results div not found or timed out for '{crop}'.")
                continue
            
            # Now extract data
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            stories_list = soup.select('.search-results .stories li a')
            
            for a_tag in stories_list:
                title = a_tag.get('title')
                if not title:
                    title = a_tag.text.strip()
                    
                href = a_tag.get('href')
                if href and not href.startswith('http'):
                    href = f"https://allafrica.com{href}"
                    
                if title and href:
                    results.append({
                        'Crop': crop,
                        'Title': title,
                        'Link': href
                    })
                    
            time.sleep(2) # polite delay between crops
            
    finally:
        driver.quit()
        
    # Write to CSV
    csv_file = "../media_data/allafrica_results.csv"
    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Crop', 'Title', 'Link'])
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        print(f"\nSaved {len(results)} results to {csv_file}")
    except Exception as e:
        print(f"Failed to write CSV: {e}")

if __name__ == "__main__":
    check_allafrica()
