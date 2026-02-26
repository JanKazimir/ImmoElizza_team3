'''import time
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


BASE_URL = "https://immovlan.be"


# This function builds the search result URL dynamically for each page
def define_url(page):
    return f"https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&islifeannuity=no&page={page}&noindex=1"


# This function collects all property links from multiple result pages
def get_property_links(pages=5):

    links = []

    with requests.Session() as s:

        headers = {"User-Agent": "Mozilla/5.0"}

        for page in range(1, pages + 1):

            url = define_url(page)

            r = s.get(url, headers=headers, timeout=10)
            print("Scraping page:", url, r.status_code)

            soup = BeautifulSoup(r.text, "html.parser")

            # Each property card contains the class below
            for card in soup.find_all("div", class_="long-and-truncated"):

                text = card.get_text(" ", strip=True)

                # Skip project sales
                if text.startswith("Project:"):
                    continue

                link = card.find("a", href=True)

                if link:
                    # urljoin automatically fixes relative or absolute URLs
                    full_link = urljoin(BASE_URL, link["href"])
                    links.append(full_link)

            time.sleep(1)

    print("Total links:", len(links))
    return links


# This function scrapes the details of a single property
def scrape_property(url, session):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    data = {}

    # Address
    address = soup.select_one(".classified__information--address")
    data["Locality"] = address.get_text(strip=True) if address else None

    # Price
    price = soup.select_one(".classified__price")
    data["Price"] = price.get_text(strip=True) if price else None

    # Features
    rows = soup.select("dl.classified__information--property, dl.classified__information--details")

    for row in rows:
        for dt, dd in zip(row.find_all("dt"), row.find_all("dd")):
            data[dt.get_text(strip=True)] = dd.get_text(strip=True)

    print(data)  # ← DEBUG

    return data


# This function manages the full scraping workflow
def scrape_dataset():

    property_links = get_property_links(pages=5)

    all_data = []

    with requests.Session() as s:

        for link in property_links:

            result = scrape_property(link, s)

            if result:
                all_data.append(result)

            time.sleep(1)

    # Write dataset to CSV only if we have data
    if all_data:

        keys = all_data[0].keys()

        with open("dataset.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, keys)
            writer.writeheader()
            writer.writerows(all_data)

        print("Dataset saved ✅")

    else:
        print("No data scraped ❌")


# Script entry point
if __name__ == "__main__":
    scrape_dataset()'''