import re
import requests
import time
import json
import csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

max_workers = 10


def get_final_list(page):
    url = page["url"]
    zip_code = page["zip"]
    dic = []

    try:
        with requests.Session() as s:
            headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
            r = s.get(url, headers=headers, timeout=10)
            time.sleep(0.2)

            if r.status_code != 200:
                return []

            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.find_all("article")
            print(f" Zip {page['zip']} elaborato ({len(articles)} annunci)")

            for article in articles:
                a_tag = article.find("a", href=True)
                if a_tag:
                    link = a_tag["href"]
                    # Assicurati che il link sia completo (aggiungi il dominio se relativo)
                    if link.startswith("/"):
                        link = "https://immovlan.be" + link
                        # salva solo se esiste davvero
                    dati = {"zip": zip_code, "url": link}
                    dic.append(dati)

    except Exception as e:
        print("errore durante il get: {}".format(e))
        return []

    # print(dic)
    return dic


with open("project_links.json", "r", encoding="utf-8") as f:
    pages_list = json.load(f)

final_list = []
count = 0
page_count = 0

print("avvio elaborazione pagine...")

with ThreadPoolExecutor(max_workers=max_workers) as executor:

    risultati = list(executor.map(get_final_list, pages_list))

for property in risultati:
    final_list.extend(property)

for i, item in enumerate(final_list, 1):
    item["id"] = i

with open("single_project_links.json", "w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=4)

print(f"Done! Projects: {len(final_list)}")
