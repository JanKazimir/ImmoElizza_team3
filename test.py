import re
import requests
import time
import json
import csv


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
    # test_zip = "2000"
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


def get_the_page():
    with requests.Session() as s:
        headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
        base_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment,student-housing,investment-property&propertysubtypes=residence,villa,bungalow,chalet,cottage,master-house,mansion,mixed-building,apartment,ground-floor,penthouse,duplex,triplex,studio,loft,student-flat,investment-property&isnewconstruction=yes&islifeannuity=no&noindex=1"
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


zip_codes = extract_zip_codes("cities.csv")
get_the_zip(zip_codes)
