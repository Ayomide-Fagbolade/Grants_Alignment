import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from secrets import ALLAFRICA_COOKIES
import urllib.parse

def parse_cookies(raw: str) -> dict:
    cookies = {}
    for part in raw.split('; '):
        part = part.strip()
        if '=' in part:
            name, _, value = part.partition('=')
            cookies[name.strip()] = urllib.parse.unquote(value)
    return cookies

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
}
cookies = parse_cookies(ALLAFRICA_COOKIES)

url = "https://allafrica.com/search/?search_string=yam&search_submit=Search"
response = requests.get(url, headers=headers, cookies=cookies)

print(f"Status Code: {response.status_code}")
print(f"Content Length: {len(response.text)}")
if "search-results" in response.text:
    print("Search results div found in raw HTML!")
else:
    print("Search results div NOT found. Content might be JS-rendered or blocked.")
    
# Let's also check advanced search
advanced_url = "https://allafrica.com/search/advanced.html"
r_adv = requests.get(advanced_url, headers=headers, cookies=cookies)
print(f"Advanced Status: {r_adv.status_code}")
