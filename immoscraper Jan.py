import time
import requests
from bs4 import BeautifulSoup
import csv




def scrape_a_page():
    pass
        
    with requests.Session() as s:
        # Variables we'll use
        url = "https://immovlan.be/en/detail/apartment/for-sale/1050/elsene/vbd89638"
        headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
        r = s.get(url, headers=headers, timeout=10 )

        print(url, r.status_code)
        soup = BeautifulSoup(r.text, "html.parser")
        print(soup)

## we can only see the first fifty pages of results, but we can hack it by changing the number in the url.
# There is a page = xx somewhere in the url. So that's a loop. We need to build a function that modifies the url for each page after the first one.

def define_url():
    ## the result of a search is a url, with a page number in it. 
    # We can't click past 49 pages of results, but we can request any page number with the url.
    # this function needs to create that url.
    pass


## this get the links of all properties, from the first page of results. 
# To do the others:
## go into the filter setting, to remove the life annuity sales.
## run it on the second page, change the url using the hack, keep going.
## we'll need to add a sleep timer function, and multithreading.
def get_pages_to_scrape():
        with requests.Session() as s:
            headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
            url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&sortdirection=ascending&sortby=zipcode&noindex=1"
            hack_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&page=4&sortdirection=ascending&sortby=zipcode&noindex=1"
            r = s.get(url, headers=headers, timeout=10 )
            print(url, r.status_code)
            soup = BeautifulSoup(r.text, "html.parser")
            links = []
            
            for card in soup.find_all("div", class_="long-and-truncated"):
                text = card.get_text(" ", strip=True)
                if text.startswith("Project: "): # if it's a project, skip it
                    continue
                link = card.find("a", href=True) 
                if link:
                    links.append(link["href"])
        
            print(links)            
        
def write_links_to_file(data):
    with open("links.csv", "w", newline="") as f:
        fieldnames=["url"]
        
        writer = csv.writer(data, fieldnames=fieldnames)
        f = writer.writeheader
        f = writer.writerows
        
        
        
 
        
get_pages_to_scrape()
    