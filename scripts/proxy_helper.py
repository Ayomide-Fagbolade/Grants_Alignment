import urllib.parse
import os
import sys

# Insert current dir to path to load secrets.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from secrets import PROXY_HOST
except ImportError:
    PROXY_HOST = "https://51.38.130.72"

TARGET_B64 = "aHR0cHM6Ly9hbGxhZnJpY2EuY29t"  # base64 of https://allafrica.com

def rewrite_to_proxy(url: str) -> str:
    """
    Rewrites https://allafrica.com/path?query to go through the proxy:
    https://51.38.130.72/path?query&__cpo=aHR0cHM6Ly9hbGxhZnJpY2EuY29t
    """
    if PROXY_HOST not in url and "allafrica.com" in url:
        parsed = urllib.parse.urlparse(url)
        path = parsed.path
        query = parsed.query
        
        # Append __cpo param
        if query:
            # Check if __cpo is already in query
            if "__cpo=" not in query:
                query += f"&__cpo={TARGET_B64}"
        else:
            query = f"__cpo={TARGET_B64}"
            
        return f"{PROXY_HOST}{path}?{query}"
    return url
