import re
import requests
from bs4 import BeautifulSoup
import time
import csv
import json



# helper function for scrape data from property page funciton
# It write the result dict as a single line, to a json


def append_dict_jsonl(record :dict, target_path):
    with open(target_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")



## This function scrapes all the data from a property link.
## it needs to be given: 
# a url to scrape
# a target file to write the data into
# a session for the request
# an index number, in case we need to restart it. 
## ❗❗❗ This function needs pages in english. Otherwise I can change it, but it's complicated sorta breaks.

        
def scrape_data_from_property_page(url, page_index, session, target_path="testing_scrape_a_page.jsonl"):
    headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
    # target_path = 

    r = session.get(url, headers=headers, timeout=10 )
    #print(url, r.status_code)
    #print("Begin Scrape!")
    soup = BeautifulSoup(r.text, "html.parser")
    
    
    ## This is the resulting dict we want: we initialise it with none values. 
    # The values found on the page are added, the rest stays as none.
    property_data = {
        "page_id": None,
        "page_url": None,
        "locality": None,
        "zip_code": None,
        "property_type": None,
        "property_subtype": None,
        "price": None,
        "number_of_bedrooms": None,
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
    property_data["page_id"] = page_index
    property_data["page_url"] = url

    ##    
    # With beautiful soup:
    ##

    # Getting the locality
    full_location = soup.find(class_="city-line")
    full_text_of_location = full_location.get_text()
    #print(full_text_of_location)
    city_text = full_text_of_location[5:]
    property_data["locality"] = city_text

    # Description
    full_description = soup.find("div", class_="dynamic-description")
    full_description_text = (full_description).get_text(strip=True)
    #property_data["description"] = full_description_text[:-17]
    
    #print(type(full_description))
    #full_description_text = full_description.get_text()
    #print(full_description_text)
    #property_data["description"] = full_description.get_text()
    
    
    # All the data from the data-rows
    for data_row in soup.find_all("div", class_="general-info-wrapper"):
        #print(f"data_row type: {type(data_row)}")
        #print(data_row)
        
        # State of property, int or none
        if data_row.find("h4", string="State of the property"):
            property_data["building_condition"] = data_row.find("h4", string="State of the property").find_next_sibling().get_text()
        
        
        # Build Year: int or none
        if data_row.find("h4", string="Build Year"):
            property_data["build_year"] = data_row.find("h4", string="Build Year").find_next_sibling().get_text()
        #else: property_data["build_year"] = "Unknown"
            
        # Terrace : True else False
        if data_row.find("h4", string="Terrace"):
            if data_row.find("h4", string="Terrace").find_next_sibling().get_text() == "Yes":
                property_data["has_terrace"] = True
            if data_row.find("h4", string="Terrace").find_next_sibling().get_text() == "No":
                property_data["has_terrace"] = False
            
        ## Terrace surface: 
        if data_row.find("h4", string="Surface terrace"):
            property_data["terrace_area_m2"] = data_row.find("h4", string="Surface terrace").find_next_sibling().get_text()
        #else: property_data["terrace_surface"] = "Unknown"
        
        # Garden : True , false or Unknown
        if data_row.find("h4", string="Garden"):
            if data_row.find("h4", string="Garden").find_next_sibling().get_text() == "Yes":
                property_data["has_garden"] = True
        #else: property_data["garden"] = False
        
        ## Garden Surface:
        if data_row.find("h4", string="Surface garden"):
            property_data["garden_area_m2"] = data_row.find("h4", string="Surface garden").find_next_sibling().get_text()
        #else: property_data["surface_garden"] = "Unknown"
        
        # Total Land surface : int or unknown
        if data_row.find("h4", string="Total land surface"):
            property_data["land_area_m2"] = data_row.find("h4", string="Total land surface").find_next_sibling().get_text()
        #else: property_data["total_land_surface"] = None

        # Furnished True, False if exists, "" if unknown
        if data_row.find("h4", string="Furnished"):
            if data_row.find("h4", string="Furnished").find_next_sibling().get_text() == "Yes":
                property_data["furnished"] = True
            else: property_data["furnished"] = False
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
        
        # Number of bedrooms:
        if data_row.find("h4", string="Number of bedrooms"):
            property_data["number_of_bedrooms"] = data_row.find("h4", string="Number of bedrooms").find_next_sibling().get_text()
        
        
            
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
    #print("Page scrapped!")
    append_dict_jsonl(property_data, target_path)
    return property_data


##
### Calling the functions for testing
##

if __name__ == "__main__":
    url = "https://immovlan.be/en/detail/ground-floor/for-sale/1050/elsene/vbd49955"        
    scrape_data_from_property_page(url)