import re
import requests
import time
import json
import csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def extract_zip_codes(file_path):
    zip_codes = []

    with open(file_path, mode="r", encoding="utf-8") as f:
        # DictReader trasforma ogni riga in un dizionario usando l'intestazione come chiave
        reader = csv.DictReader(f)

        for row in reader:
            # Sostituisci 'zipCode' con il nome esatto della colonna nel tuo CSV
            zip_val = row.get("zipCode")
            if zip_val and zip_val not in zip_codes:
                zip_codes.append(zip_val)

    return zip_codes


def get_the_zip(zlista):
    # in: lista zip codes
    # out: lista slug
    slug_list = []
    to_do_list = []
    for zip in zlista:
        api_url = (
            f"https://immovlan.be/en/api/core/autocomplete?query={zip}&countryId=318"
        )

        # Aggiungiamo l'identità del browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # Verifichiamo se la risposta è andata a buon fine (200)
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            if response.status_code == 200:
                json_r = response.json()
                print(json_r)
                lista_res = json_r.get("data", [])
                len_res = len(lista_res)
                if len_res > 1:
                    risultato = lista_res[1]
                    slug = risultato.get("slug")
                    if slug and slug not in slug_list:
                        slug_list.append(slug)
                elif len_res == 1:
                    risultato = lista_res[0]
                    slug = risultato.get("slug")
                    if slug and slug not in slug_list:
                        slug_list.append(slug)

            elif response.status_code == 429:
                print("Troppe richieste! Pausa forzata...")
                time.sleep(30)

        except requests.exceptions.Timeout:
            print(f"!! Timeout su {zip}: il server non ha risposto. Salto...")
            to_do_list.append(zip)
        except Exception as e:
            print("Errore al codice zip:{}, errore: {}".format(zip, e))
            to_do_list.append(zip)

        if len(slug_list) % 50 == 0 and len(slug_list) > 0:
            with open("slugs_list_BACKUP.json", "w") as f:
                json.dump(slug_list, f, indent=4)
            with open("to_do_slug.json", "w") as file:
                json.dump(to_do_list, file, indent=4)

        time.sleep(0.2)

    with open("slugs_list.json", "w") as f:
        json.dump(slug_list, f, indent=4)
    print("File salvato con successo!, {} slug unici salvati".format(len(slug_list)))


def get_the_urls(json_input, json_output):
    # in: lista degli slug
    # out: dizionario zip - url
    with open(json_input, "r", encoding="utf-8") as f:
        slugs = json.load(f)

    url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment,student-housing,investment-property&propertysubtypes=residence,villa,bungalow,chalet,cottage,master-house,mansion,mixed-building,apartment,ground-floor,penthouse,duplex,triplex,studio,loft,student-flat,investment-property&towns=1000-brussels&noindex=1"
    # regex per sostituire lo slug
    # nel ciclo for, salvo anche lo zip
    pattern = r"(.*towns=)[^&]+(&.*)"
    match = re.search(pattern, url)

    if not match:
        print("Errore: Impossibile trovare il parametro 'towns' nell'URL base.")
        return None

    prefix = match.group(1)
    suffix = match.group(2)
    urls_dict = {}

    for slug in slugs:
        urls_dict[slug] = "{}{}{}".format(prefix, slug, suffix)

    with open(json_output, "w", encoding="utf-8") as file:
        json.dump(urls_dict, file, indent=4)

    print(f"Dizionario creato con successo! Generati {len(urls_dict)} URL.")
    return urls_dict


def get_the_page():
    with requests.Session() as s:
        headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
        base_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=apartment,investment-property,house,student-housing&propertysubtypes=apartment,studio,penthouse,duplex,ground-floor,loft,investment-property,residence,master-house,mixed-building,student-flat&towns=2000-antwerp&noindex=1"
        n = 1
        pages_dict = {}
        pages_dict["page 1"] = base_url
        pattern = r"(&noindex=1)"

        for n in range(2, 5):
            url = re.sub(pattern, f"&page={n}\\1", base_url)
            pages_dict["page {}".format(n)] = url
            r = s.get(base_url, headers=headers, timeout=10)

            if r.status_code != 200 or "No results found" in r.text:
                print("End of pages!")
                break

        print("ecco il dizionario ^: {}".format(pages_dict))
        return pages_dict


def has_results(html_content):
    """
    Controlla se nella pagina non è vuota --> sono presenti annunci immobiliari cercandoli per tag.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Cerchiamo tutti i tag <article>
    # Se vuoi essere più preciso, aggiungi la classe: soup.find_all('article', class_='nome-classe')
    listings = soup.find_all("article")

    # Se la lista non è vuota, abbiamo trovato degli immobili
    if len(listings) > 0:
        return True
    return False


def get_the_pages(url):
    with requests.Session() as s:
        headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
        lista = []
        pattern = r"(&noindex=1)"
        n = 0
        match = re.search(r"towns=([^&]+)", url)
        if match:
            slug = match.group(1)
        while True:
            n += 1
            base_url = re.sub(pattern, f"&page={n}\\1", url)
            try:
                r = s.get(base_url, headers=headers, timeout=10)

                if r.status_code == 200 and has_results(r.text):
                    lista.append({"zip": slug, "page": n, "url": base_url})
                    time.sleep(0.2)
                else:
                    # Se la pagina è vuota o il server dà errore, usciamo dal ciclo per questo ZIP
                    print(f"Fine pagine per {slug}. Totale: {n-1}")
                    break

            except Exception as e:
                print("Errore: {}".format(e))

    print("lista creata con successo: {}".format(lista))
    return lista


"""
with open("urls_dict.json", "r", encoding="utf-8") as f:
    data = json.load(f)

lista_completa = []

for zip, url in data.items():
    print("elaborazione zip {}".format(zip))
    lista = get_the_pages(url)
    lista_completa.extend(lista)
    if len(lista_completa) % 20 == 0:
        with open("emergency_backup.json", "w", encoding="utf-8") as f:
            json.dump(lista_completa, f, indent=4)

with open("pages.json", "w", encoding="utf-8") as f:
    json.dump(lista_completa, f, indent=4)

print(f"Operazione conclusa! Totale URL pronti per lo scraping: {len(lista_completa)}")
"""

max_workers = 10


def get_final_list(page):
    url = page["url"]
    zip_code = page["zip"]
    dic = []
    pdic = []
    try:
        with requests.Session() as s:
            headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
            r = s.get(url, headers=headers, timeout=10)
            print(f"✅ Zip {page['zip']} elaborato ({len(articles)} annunci)")

            time.sleep(0.2)

            if r.status_code != 200:
                return [], []

            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.find_all("article")

            for article in articles:
                a_tag = article.find("a", href=True)
                if a_tag:
                    link = a_tag["href"]
                    # Assicurati che il link sia completo (aggiungi il dominio se relativo)
                    if link.startswith("/"):
                        link = "https://immovlan.be" + link
                        # salva solo se esiste davvero
                    dati = {"zip": zip_code, "url": link}

                    if "/projectdetail/" in link:
                        pdic.append(dati)
                    else:
                        dic.append(dati)

    except Exception as e:
        print("errore durante il get: {}".format(e))
        return [], []

    # print(dic)
    return dic, pdic


with open("pages.json", "r", encoding="utf-8") as f:
    pages_list = json.load(f)

final_list = []
project_list = []
count = 0
page_count = 0

print("avvio elaborazione pagine...")

with ThreadPoolExecutor(max_workers=max_workers) as executor:

    risultati = list(executor.map(get_final_list, pages_list))

for property, project in risultati:
    final_list.extend(property)
    project_list.extend(project)

for i, item in enumerate(final_list, 1):
    item["id"] = i

for j, item in enumerate(project_list, 1):
    item["id"] = j

with open("links.json", "w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=4)
with open("project_links.json", "w", encoding="utf-8") as f:
    json.dump(project_list, f, indent=4)


print(f"Fatto! Annunci: {len(final_list)} | Progetti: {len(project_list)}")

# get_final_list("https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment,student-housing,investment-property&propertysubtypes=residence,villa,bungalow,chalet,cottage,master-house,mansion,mixed-building,apartment,ground-floor,penthouse,duplex,triplex,studio,loft,student-flat,investment-property&towns=3800-aalst&page=2&noindex=1")


# get_the_urls("slugs_list.json", "urls_dict.json")
# zip_codes = extract_zip_codes("cities.csv")
# get_the_zip(zip_codes)
# https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=apartment,investment-property,house,student-housing&propertysubtypes=apartment,studio,penthouse,duplex,ground-floor,loft,investment-property,residence,master-house,mixed-building,student-flat&towns=2000-antwerp&noindex=1
# https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=apartment,investment-property,house,student-housing&propertysubtypes=apartment,studio,penthouse,duplex,ground-floor,loft,investment-property,residence,master-house,mixed-building,student-flat&towns=2000-antwerp&page=7&noindex=1


"""
with open("pages.json", "r", encoding="utf-8") as f:
    pages_list = json.load(f)

final_list = []
count = 0
page_count = 0
for i, page in enumerate(pages_list):
    page_count += 1
    print(
        " {} / {} ... Elaborazione  zip {}".format(i + 1, len(pages_list), page["zip"])
    )
    link = get_final_list(page["url"])

    if not link:
        continue

    for url_property in link.values():
        count += 1
        # Creiamo un oggetto pulito per ogni singola proprietà
        proprieta = {"id": count, "zip": page["zip"], "url": url_property}
        final_list.append(proprieta)

    if page_count % 20 == 0:
        with open("pr_emergency_backup.json", "w", encoding="utf-8") as f:
            json.dump(final_list, f, indent=4)
            print(f"--- Backup salvato a quota {count} immobili ---")

    time.sleep(0.1)

with open("links.json", "w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=4)

print(f"Fatto! Totale proprietà salvate: {count}")
"""
