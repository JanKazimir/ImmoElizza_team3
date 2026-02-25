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
    "page_id": int,                     
    "page_url": str,                    
    "locality": str,                    
    "property_type": str,               
    "property_subtype": str,          
    "price": float | int | None,        
    "number_of_rooms": int | None,
    "living_area_m2": float | int | None,
    ""kitchen_equipment"": str | None,
    "furnished": bool | None,
    "has_terrace": bool | None,
    "terrace_area_m2": float | int | None,   
    "has_garden": bool | None,
    "garden_area_m2": float | int | None,   
    "land_area_m2": float | int | None,      
    "number_of_facades": int | None,
    "has_swimming_pool": bool | None,
    "building_condition": str, 
    "build_year": int
}
 """

def append_dict_jsonl(path, record :dict):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# This is the function so far.
# Let's get one data field at a time, starting with url

def scrape_a_page(url):
        with requests.Session() as s:
            headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}

            r = s.get(url, headers=headers, timeout=10 )
            print(url, r.status_code)
            print("Begin Scrape!")
            soup = BeautifulSoup(r.text, "html.parser")
            #tree = html.fromstring(r.text)
            
            url = url

            property_data = {
                "page_id": None,
                "page_url": None,
                "locality": None,
                "zip_code": None,
                "property_type": None,
                "property_subtype": None,
                "price": None,
                "number_of_rooms": None,
                "livable_surface_m2": None,
                "kitchen_equipment": None,
                "furnished": None,
                "has_terrace": None,
                "terrace_area_m2": None,
                "has_garden": None,
                "garden_area_m2": None,
                "land_area_m2": None,
                "number_of_facades": None,
                "has_swimming_pool": None,
                "building_condition": None,
                "build_year": None,
            }
            
            # page id is for restarting in case we need to.
            property_data["page_id"] = 1
            
            property_data["page_url"] = url

            # this is with beautiful soup:
            #location_block = soup.find("div", class_="d-lg-block d-none")
            #if location_block:
            full_location = soup.find(class_="city-line")
            full_text_of_location = full_location.get_text()
            #print(full_text_of_location)
            city_text = full_text_of_location[5:]
            property_data["locality"] = city_text

          
            
            # All the data from the rows
            for data_row in soup.find_all("div", class_="general-info-wrapper"):
                #print(f"data_row type: {type(data_row)}")
                #print(data_row)
                
                # State of property, int or if not : unknown
                if data_row.find("h4", string="State of the property"):
                    property_data["building_condition"] = data_row.find("h4", string="State of the property").find_next_sibling().get_text()
               
               
                # Build Year: int or F
                if data_row.find("h4", string="Build Year"):
                    property_data["build_year"] = data_row.find("h4", string="Build Year").find_next_sibling().get_text()
                #else: property_data["build_year"] = "Unknown"
                    
                # Terrace : True else False
                if data_row.find("h4", string="Terrace"):
                    if data_row.find("h4", string="Terrace").find_next_sibling().get_text() == "Yes":
                        property_data["terrace"] = True
                    if data_row.find("h4", string="Terrace").find_next_sibling().get_text() == "No":
                       property_data["terrace"] = False
                    
                ## Terrace surface: 
                if data_row.find("h4", string="Surface terrace"):
                    property_data["terrace_surface"] = data_row.find("h4", string="Surface terrace").find_next_sibling().get_text()
                #else: property_data["terrace_surface"] = "Unknown"
                
                # Garden : True , false or Unknown
                if data_row.find("h4", string="Garden"):
                    if data_row.find("h4", string="Garden").find_next_sibling().get_text() == "Yes":
                        property_data["garden"] = True
                #else: property_data["garden"] = False
                
                ## Garden Surface:
                if data_row.find("h4", string="Surface garden"):
                    property_data["surface_garden"] = data_row.find("h4", string="Surface garden").find_next_sibling().get_text()
                #else: property_data["surface_garden"] = "Unknown"
                
                # Total Land surface : int or unknown
                if data_row.find("h4", string="Total land surface"):
                    property_data["total_land_surface"] = data_row.find("h4", string="Total land surface").find_next_sibling().get_text()
                #else: property_data["total_land_surface"] = None

                # Furnished True, False if exists, "" if unknown
                if data_row.find("h4", string="Furnished"):
                    if data_row.find("h4", string="Furnished").find_next_sibling().get_text() == "Yes":
                        property_data["Furnished"] = True
                    else: property_data["Furnished"] = False
                #else: property_data["Furnished"] = ""
                
                # Facades: int 
                if data_row.find("h4", string="Number of facades"):
                    property_data["number_of_facades"] = data_row.find("h4", string="Number of facades").find_next_sibling().get_text()
                    
                # Swimming pool: True Or False
                if data_row.find("h4", string="Swimming pool"):
                    if data_row.find("h4", string="Swimming pool") == "Yes":
                        property_data["has_swimming_pool"] = True
                    else: property_data["has_swimming_pool"] = False
                    
                # Kitchen Equipment:
                if data_row.find("h4", string="Kitchen equipment"):
                    property_data["kitchen_equipment"] = data_row.find("h4", string="Kitchen equipment").find_next_sibling().get_text()
                    
                # .find_next_sibling().get_text()
                

            ## Magic block has a lot of stuff:
            for magicbox in soup.find_all("script", type="text/javascript"):
                magic_text = magicbox.get_text()
                magic_block = re.search(r"dataLayer\.push\(\s*(\{[^}]*\})\s*\|\|", magic_text, re.S)
                if magic_block:
                    magic_data = json.loads(magic_block.group(1))
                    property_data["price"] = int(float(magic_data.get("price")))
                    property_data["property_type"] = magic_data.get("property_type")
                    property_data["property_subtype"] = magic_data.get("property_sub_type")
                    property_data["livable_surface_m2"] = int(float(magic_data.get("livable_surface")))
                    property_data["zip_code"] = magic_data.get("zip_code")
                    break
            

            #print(property_data)
            append_dict_jsonl("testing_scrape_a_page.jsonl", property_data)
            return property_data
        
url = "https://immovlan.be/en/detail/apartment/for-sale/1050/elsene/vbd89639"        
scrape_a_page(url)


        
       
