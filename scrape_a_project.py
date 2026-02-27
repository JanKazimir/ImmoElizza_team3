import re
import requests
from bs4 import BeautifulSoup
import time
import csv
import json

from scrape_a_property_page import append_dict_jsonl


def scrape_data_from_property_page(
    url, page_index, session, target_path="testing_scrape_a_page.jsonl"
):
    headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}

    # 1. Inizializza property_data QUI (fuori dal try)
    property_data = {
        "page_id": page_index,
        "page_url": url,
        "locality": None,
        "zip_code": None,
        "property_type": None,
        "property_subtype": None,
        "price": None,
        "number_of_bedrooms": None,
        "livable_surface_m2": None,
        "kitchen_equipment": None,
        "furnished": None,
        "has_terrace": None,
        "terrace_area_m2": None,
        "has_garden": None,
        "garden_area_m2": None,
        "land_area_m2": None,
        "number_of_facades": None,
        "has_swimming_pool": None,
        "building_condition": None,
        "build_year": None,
    }

    # 2. Se session è None (come nel tuo test), creane una temporanea
    if session is None:
        session = requests.Session()

    try:
        r = session.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")

        # ... (Tutto il resto del tuo codice BeautifulSoup rimane identico) ...
        # (Assicurati solo di NON ri-dichiarare property_data = {...} dentro il try)

        # Getting the locality
        full_location = soup.find(class_="city-line")
        if full_location:
            city_text = full_location.get_text(strip=True)[5:]
            property_data["locality"] = city_text

        # ... e così via per tutti i campi ...

        # Blocco Magic DataLayer
        for magicbox in soup.find_all("script", type="text/javascript"):
            magic_text = magicbox.get_text()
            magic_block = re.search(
                r"dataLayer\.push\(\s*(\{[^}]*\})\s*\|\|", magic_text, re.S
            )
            if magic_block:
                try:
                    magic_data = json.loads(magic_block.group(1))
                    # Usiamo .get() con cautela
                    p = magic_data.get("price")
                    if p:
                        property_data["price"] = int(float(p))

                    property_data["property_type"] = magic_data.get("property_type")
                    property_data["property_subtype"] = magic_data.get(
                        "property_sub_type"
                    )

                    s = magic_data.get("livable_surface")
                    if s:
                        property_data["livable_surface_m2"] = int(float(s))

                    property_data["zip_code"] = magic_data.get("zip_code")
                except:
                    pass
                break

    except Exception as e:
        print("errore su {} : {}".format(url, e))
        # Se c'è un errore critico (es. internet staccato), meglio non salvare nulla
        return None

    # Ora property_data esiste sicuramente, quindi non crasherà più qui
    append_dict_jsonl(property_data, target_path)
    return property_data


url = "https://immovlan.be/en/detail/studio/for-sale/1000/brussels/vbd90094"
scrape_data_from_property_page(
    url, page_index=1, session=None, target_path="testing_scrape_a_page.jsonl"
)
