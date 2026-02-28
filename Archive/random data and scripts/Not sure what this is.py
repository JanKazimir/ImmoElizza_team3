import requests
from bs4 import BeautifulSoup

urls = [
    "https://immovlan.be/fr/detail/duplex/a-louer/1000/bruxelles/vbd86919",
    "https://immovlan.be/en/projectdetail/25923-7585534",
    "https://immovlan.be/en/detail/residence/for-sale/9040/sint-amandsberg/rbv27777",
    "https://immovlan.be/en/detail/penthouse/for-sale/9000/gent/rbv26652",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

for url in urls:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    desc_tag = soup.find("meta", {"name": "description"})

    if desc_tag:
        print("URL:", url)
        print("DESCRIPTION:", desc_tag["content"])
        print("-" * 50)
    else:
        print("Description yok →", url)