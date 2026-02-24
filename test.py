import re
import requests


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


get_the_page()
