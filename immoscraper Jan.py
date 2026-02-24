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
### look into asyncio and aiohttp library. to make lots of requests in parrallel

def get_pages_to_scrape():
        with requests.Session() as s:
            headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
            url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&sortdirection=ascending&sortby=zipcode&noindex=1"
            hack_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&page=4&sortdirection=ascending&sortby=zipcode&noindex=1"
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


## Not sure about this: 
### we should also write a url id, in case we need it for the loops       
def write_links_to_file(data):
    with open("links.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames= ["id", "url"]
        
        writer = csv.writer(f, fieldnames=fieldnames)
        writer.writeheader
        writer.writerows(data)
        
        
 
just_in_case_links = ['https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd86951', 'https://immovlan.be/en/detail/villa/for-sale/1000/brussels/rbv09716', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd90215', 'https://immovlan.be/en/detail/studio/for-sale/1000/brussels/vbd90167', 'https://immovlan.be/en/detail/ground-floor/for-sale/1000/brussels/vbd90166', 'https://immovlan.be/en/detail/loft/for-sale/1000/brussels/vbd90160', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd89713', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/rbv33376', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd89582', 'https://immovlan.be/en/detail/penthouse/for-sale/1000/brussels/vbd89485', 'https://immovlan.be/en/detail/master-house/for-sale/1000/brussels/vbd89465', 'https://immovlan.be/en/detail/studio/for-sale/1000/brussels/vbd89451', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd89450']
 
        
#get_pages_to_scrape()
write_links_to_file(just_in_case_links)

    