# first line: 47
import logging

from bs4 import BeautifulSoup
from fastapi import requests
from joblib import memory


@memory.cache
def fetch_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if "text/html" not in res.headers.get("Content-Type", ""):
            return ""
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.extract()
        text = "\n".join(tag.get_text(strip=True) for tag in soup.find_all(["h1", "h2", "p", "li"]))
        return text
    except Exception as e:
        logging.warning(f"Failed to fetch {url}: {e}")
        return ""
