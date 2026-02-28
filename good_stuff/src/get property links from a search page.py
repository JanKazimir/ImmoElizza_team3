import requests
from bs4 import BeautifulSoup



## this get the links of all properties, from the first page of results. 
def get_twenty_property_links_from_a_search_page():
        with requests.Session() as s:
            headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
            url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&propertysubtypes=residence,chalet,bungalow,villa,apartment,duplex,loft,penthouse&islifeannuity=no&page=5&noindex=1"
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


        
#get_pages_to_scrape()