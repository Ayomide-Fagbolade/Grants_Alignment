import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from secrets import ALLAFRICA_COOKIES

def parse_cookies(raw: str) -> list[dict]:
    """Parse a cookie string into a list of dicts for Selenium add_cookie()."""
    cookies = []
    for part in raw.split('; '):
        part = part.strip()
        if '=' in part:
            name, _, value = part.partition('=')
            value = urllib.parse.unquote(value)
            cookies.append({
                'name': name.strip(),
                'value': value,
                'domain': '.allafrica.com',
                'path': '/',
            })
    return cookies


def make_driver() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
    )
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(15)

    # Navigate to the domain first, then inject cookies
    driver.get("https://allafrica.com")
    for cookie in parse_cookies(ALLAFRICA_COOKIES):
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass

    return driver
