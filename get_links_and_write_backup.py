# voglio una funzione che mi parta dal link base
# e che restituisca un dizionario {page N = url}

import re
import requests
import csv
import time
import requests
from bs4 import BeautifulSoup
import csv

def write_links_to_file(links_as_dict):
    with open("test_links.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames= ["page_number", "url"]
        writer = csv.writer(f)
        writer.writerow(["page_number", "url"])
        
        for page_number, links in links_as_dict.items():
            for url in links:
                writer.writerow([page_number, url])



def create_base_file(name):
    with open(f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["page_number", "url"])

# This is from edo and me
def get_the_page():
    with requests.Session() as s:
        headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
        
        # first try with the lux province
        base_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&propertysubtypes=residence,chalet,bungalow,villa,apartment,duplex,loft,penthouse&provinces=luxembourg&islifeannuity=no&page="
        end_url = "&sortdirection=ascending&sortby=zipcode&noindex=1"
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
        write_links_to_file(pages_dict)
        return pages_dict



def get_pages_to_scrape(url):
        with requests.Session() as s:
            headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
            #url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&propertysubtypes=residence,chalet,bungalow,villa,apartment,duplex,loft,penthouse&islifeannuity=no&page=5&noindex=1"
            r = s.get(url, headers=headers, timeout=10 )
            print(url, r.status_code)
            soup = BeautifulSoup(r.text, "html.parser")
            links = []
            
            # get all the links from a single page result
            for card in soup.find_all("div", class_="long-and-truncated"):
                text = card.get_text(" ", strip=True)
                if text.startswith("Project: "): # if it's a project, skip it
                    continue
                link = card.find("a", href=True) 
                if link:
                    links.append(link["href"])
        
            print(links)
            return links




#get_the_page()
list_of_pages = []


## This function works for getting all the links for luxembourg.
# i need to modify it to get all the links from the reverse order, so i can run it on the rest of the provinces.
def get_links_and_write_to_file():
    with requests.Session() as s:
        headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
        # first try with the lux province
        base_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&propertysubtypes=residence,chalet,bungalow,villa,apartment,duplex,loft,penthouse&provinces=luxembourg&islifeannuity=no&page="
        end_url = "&sortdirection=ascending&sortby=zipcode&noindex=1"
        pages_of_results = range(1, 50)
        for i in pages_of_results:
            lux_all_pages_dict = {}
            url = base_url+f"{i}"+end_url
            #list_of_pages.append(url)
            lux_all_pages_dict[i] = get_pages_to_scrape(url)
            append_links_to_file(lux_all_pages_dict)
            
            
    return lux_all_pages_dict

def get_links_and_write_to_file_with_reverse(province):
    with requests.Session() as s:
        headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
        # trying with province as placeholder
        ## This time namur
        full_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&propertysubtypes=residence,mixed-building,villa,cottage,bungalow,master-house,chalet,mansion,apartment,penthouse,ground-floor,duplex,loft,studio,triplex&provinces=namur&isnewconstruction=yes&islifeannuity=no&page=2&sortdirection=ascending&sortby=zipcode&noindex=1"
        base_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&propertysubtypes=residence,mixed-building,villa,cottage,bungalow,master-house,chalet,mansion,apartment,penthouse,ground-floor,duplex,loft,studio,triplex&provinces=namur&isnewconstruction=yes&islifeannuity=no&page="
        
        ascending_end_url = "&sortdirection=ascending&sortby=zipcode&noindex=1"
        descending_end_url = "&sortdirection=descending&sortby=zipcode&noindex=1"
        file_name = f"{province}_all_links"
        create_base_file(file_name)
        
        ## !! Don't forget to update the range of the second loop
 
        ## grabbing the first 1000 in ascending order:
        pages_of_results = range(1, 51)
        for i in pages_of_results:
            all_pages_dict = {}
            url = base_url+f"{i}"+ascending_end_url
            #list_of_pages.append(url)
            all_pages_dict[i] = get_pages_to_scrape(url)
            append_links_to_file(file_name, all_pages_dict)
        
        ## update the range here : One more than the target.
        ## Grabbing the rest, in descending order
        for i in range(1, 34):
            all_pages_dict = {}
            url = base_url+f"{i}"+descending_end_url
            #list_of_pages.append(url)
            all_pages_dict[f"{50+i}"] = get_pages_to_scrape(url)
            append_links_to_file(file_name, all_pages_dict)
                
            
    return all_pages_dict

## this is the url for sorting from high to low the brabant wallon province:
# https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&propertysubtypes=residence,chalet,bungalow,villa,apartment,duplex,loft,penthouse&provinces=brabant-wallon&islifeannuity=no&sortdirection=descending&sortby=zipcode&noindex=1
## this one in reverse order, starting on page 2
# https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&propertysubtypes=residence,chalet,bungalow,villa,apartment,duplex,loft,penthouse&provinces=brabant-wallon&islifeannuity=no&page=2&sortdirection=descending&sortby=zipcode&noindex=1
            
            
def append_links_to_file(name, links_as_dict):
    with open(f"{name}.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        #writer.writerow(["page_number", "url"])
        
        for page_number, links in links_as_dict.items():
            for url in links:
                writer.writerow([page_number, url])                 


        
def append_links_to_file_with_reversed(name, links_as_dict, reversed=False):
    with open(f"{name}.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        #writer.writerow(["page_number", "url"])
        
        for page_number, links in links_as_dict.items():
            for url in links:
                writer.writerow([reversed, page_number, url])           



        
#get_the_page()        
        
        
#get_links_and_write_to_file()   
#print(list_of_pages)

def write_list_to_csv(rows, file_path, header=None):
    """
    rows: list of lists/tuples (e.g. [[1, "a"], [2, "b"]])
    header: optional list for column names
    """
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        writer.writerows([[item]for item in rows])


#write_list_to_csv(list_of_pages, "listofluxresultspages.csv")

get_links_and_write_to_file_with_reverse("namur")