import urllib.parse
import os
import sys
import importlib.util

# Load secrets.py directly by path — avoids clashing with the stdlib 'secrets' module
_spec = importlib.util.spec_from_file_location(
    "allafrica_secrets",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "secrets.py")
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
PROXY_HOST = getattr(_mod, "PROXY_HOST", "https://185.16.38.230")

TARGET_B64 = "aHR0cHM6Ly9hbGxhZnJpY2EuY29t"  # base64 of https://allafrica.com

def rewrite_to_proxy(url: str) -> str:
    """
    Rewrites https://allafrica.com/path?query to go through the proxy:
    https://185.16.38.230/path?query&__cpo=aHR0cHM6Ly9hbGxhZnJpY2EuY29t
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