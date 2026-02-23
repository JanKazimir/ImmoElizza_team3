import time
import requests
from bs4 import BeautifulSoup

def scrape_a_page():
        
    with requests.Session() as s:
        # Variables we'll use
        url = "https://immovlan.be/en/detail/apartment/for-sale/1050/elsene/vbd89638"
        headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
        
        
        s = requests.Session()
        r = s.get(url, headers=headers, timeout=10 )

        print(url, r.status_code)
        soup = BeautifulSoup(r.text, "html.parser")
        print(soup)
