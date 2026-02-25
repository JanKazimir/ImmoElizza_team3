import re
import requests
import csv
import time
import requests
from bs4 import BeautifulSoup
import csv
import json


# This is the function that will scrape a page of all the usefull data. 
# Return a dict, with an index number and url as key.

## Target Dict:

""" 
property_data = {
    "page_id": int,
    "page_url": str,                 
    "locality": str,                    
    "property_type": str,               
    "property_subtype": str,          
    "price": float | int | None,        # <span class="detail__header_price_data"> <small></small> 235 000 €<small></small> </span>
    "number_of_rooms": int | None,
    "living_area_m2": float | int | None,
    "kitchen_fully_equipped": bool | None,
    "furnished": bool | None,
    "open_fire": bool | None,
    "has_terrace": bool | None,
    "terrace_area_m2": float | int | None,   
    "has_garden": bool | None,
    "garden_area_m2": float | int | None,   
    "land_area_m2": float | int | None,      
    "number_of_facades": int | None,
    "has_swimming_pool": bool | None,
    "building_condition": str
}

        

 """


# This is the function so far.
# Let's get one data field at a time, starting with url

def scrape_a_page(url, page_id=1):
        with requests.Session() as s:
            headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}

            r = s.get(url, headers=headers, timeout=10 )
            print(url, r.status_code)
            print("Begin Scrape!")
            soup = BeautifulSoup(r.text, "html.parser")
            print(soup)
            
            #url = "https://immovlan.be/en/detail/duplex/for-sale/3630/meeswijk/rwc41877"
            page_id = 1
            property_data = {}
            property_data["page_id"] = page_id
            property_data["page_url"] = url
            #property_data["price"] = price
            
            soup_price = soup.find_all("div", class_="detail__header_price_data")
            print(soup_price)
            
               # :
               # soup.get_text(" ", strip=True) 
                
                #if text.startswith("Project: "): # if it's a project, skip it

               # link = card.find("a", href=True) 

        
            print(property_data)
            return property_data
        
url = "https://immovlan.be/en/detail/duplex/for-sale/3630/meeswijk/rwc41877"        
scrape_a_page(url)
        
       
