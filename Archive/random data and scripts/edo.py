# voglio una funzione che mi parta dal link base
# e che restituisca un dizionario {page N = url}

import re
import requests


def get_the_page():
    with requests.Session() as s:
        headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
        base_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment,student-housing,investment-property&propertysubtypes=residence,villa,bungalow,chalet,cottage,master-house,mansion,mixed-building,apartment,ground-floor,penthouse,duplex,triplex,studio,loft,student-flat,investment-property&isnewconstruction=yes&islifeannuity=no&noindex=1"
        n = 1
        pages_dict = {}
        pages_dict[n] = base_url
        pattern = r"(&noindex=1)"

        while True:
            n += 1
            r = s.get(base_url, headers=headers, timeout=10)
            print(
                f"Scaricando pagina {n}...", end="\r"
            )  # end='\r' sovrascrive la stessa riga, molto pulito!

            if r.status_code != 200 or "No results found" in r.text:
                print("End of pages!")
                break

            # if n > 20:  # Fermati dopo 20 pagine per vedere se il dizionario è corretto
            # print("\nTest completato con successo (prime 20 pagine).")
            # break

            url = re.sub(pattern, f"&page={n}\\1", base_url)
            pages_dict[n] = url

        print("ecco il dizionario ^: {}".format(pages_dict))
        return pages_dict


get_the_page()
