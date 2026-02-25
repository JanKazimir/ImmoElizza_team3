import re
import requests
import csv
import time
import requests
from bs4 import BeautifulSoup
import csv
import json
from lxml import html

# This is the function that will scrape a page of all the usefull data. 
# Return a dict, with an index number and url as key.

## Target Dict:

""" 
property_data = {
    "page_id": int,                     # index, set as default for now
    "page_url": str,                    # done
    "locality": str,                    
    "property_type": str,               # houses, appartment, investment property
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
            tree = html.fromstring(r.content)
            #print(soup)
            
            #url = "https://immovlan.be/en/detail/duplex/for-sale/3630/meeswijk/rwc41877"

            property_data = {}
            property_data["page_id"] = page_id
            property_data["page_url"] = url
            
            ## Magic block has a lot of stuff:
            for magicbox in soup.find_all("script", type="text/javascript"):
                magic_text = magicbox.get_text()
                magic_block = re.search(r"dataLayer\.push\(\s*(\{[^}]*\})\s*\|\|", magic_text, re.S)
                if magic_block:
                    magic_data = json.loads(magic_block.group(1))
                    property_data["price"] = magic_data.get("price")
                    property_data["property_type"] = magic_data.get("property_type")
                    property_data["property_sub_type"] = magic_data.get("property_sub_type")
                    property_data["livable_surface_m2"] = magic_data.get("livable_surface")
                    property_data["zip_code"] = magic_data.get("zip_code")
                    break
            
            ## need to get into data rows now: number of rooms, kitchen_fully_equipped(bool), 
            # furnished bool, fire bool, terrace bool, terrace aream2,
            # has garden bool, garden area, num of facades, swimming pool bool 
            
            #trying with Xpath:
            
            num_bedrooms_tree = tree.xpath("/html/body/div[2]/div[4]/div[3]/div[8]/div/div[2]/div/div[1]/p")
            print(num_bedrooms_tree[0].text_content())
            if num_bedrooms_tree:
                num_bedrooms = num_bedrooms_tree[0].text_content().strip()
                print(f"number of bedrooms is : {num_bedrooms}")
            
            # this is with beautiful soup:
            #for data_row in soup.find_all("div", class_="general-info-wrapper"):
            #    for data_row_wrapper in data_row:
            #        wrapper = data_row_wrapper.get_text(" ", strip=True)
            #        print(wrapper)
            
            
            
            

        
            print(property_data)
            return property_data
        
url = "https://immovlan.be/en/detail/duplex/for-sale/3630/meeswijk/rwc41877"        
scrape_a_page(url)
        
       
