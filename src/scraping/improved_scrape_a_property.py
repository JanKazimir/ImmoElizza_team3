import re
import requests
from bs4 import BeautifulSoup
import time
import csv
import json

###
###
## This is the improved function to scrape the data from a property page. Based on edo's improved version. 
###
###


# helper function for scrape data from property page funciton
# It write the result dict as a single line, to a json
def append_dict_jsonl(record: dict, target_path):
    with open(target_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


## This function scrapes all the data from a property link.
## it needs:
# a url to scrape
# a target file to write the data into
# a session for the request
# an index number, in case we need to restart it.
## ❗❗❗ This function needs pages in english. Otherwise I can change it, but it's complicated sorta breaks.


def improved_scrape_data_from_property_page(
    url, page_index, session, target_path="testing_scrape_a_page.jsonl"
):
    headers = {"User-Agent": "Chrome", "Connection": "keep-alive"}
    # target_path =

    try:
        r = session.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        #print(soup)

        ## This is the resulting dict we want: we initialise it with none values.
        # The values found on the page are added, the rest stays as none.
        property_data = {
            "page_id": page_index,
            "page_url": url,
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
            "has_cellar": None,
            "has_garage": None,
            "number_of_garages": None,
            "type_of_heating": None,
            "has_elevator": None,
            "has_access_for_disabled": None,
            "is_low_energy": None,
            "has_solar_panels": None,
            "has_floor_heating": None,
            "has_heat_pump": None,
            "has_fireplace": None,
            "has_balcony": None,
            "type_of_glazing": None,
            "specific_primary_energy_consumption_KWh_by_m2_by_year": None,
            "has_attic": None,
            "yearly_total_primary_energy_consumption_in_kWh_by_year": None, 
            "description": None    
        }

        # Getting the locality
        full_location = soup.find(class_="city-line")
        if full_location:
            full_text_of_location = full_location.get_text(strip=True)
            # print(full_text_of_location)
            city_text = full_text_of_location[5:]
            property_data["locality"] = city_text

        # Description
        full_description = soup.find("div", class_="dynamic-description")
        if full_description:
            full_description_text = (full_description).get_text(strip=True)
            property_data["description"] = full_description_text[:-17]


        # All the data from the data-rows
        for data_row in soup.find_all("div", class_="general-info-wrapper"):
            # print(f"data_row type: {type(data_row)}")
            # print(data_row)

            # State of property, int or none
            if data_row.find("h4", string="State of the property"):
                property_data["building_condition"] = (data_row.find("h4", string="State of the property").find_next_sibling().get_text())
            
            # Cellar : Bool    
            if data_row.find("h4", string="Cellar"):
                if data_row.find("h4", string="Cellar").find_next_sibling().get_text() == "Yes":
                    property_data["has_cellar"] = True
                if data_row.find("h4", string="Cellar").find_next_sibling().get_text() == "No":
                    property_data["has_cellar"] = False

            # Garage : Bool    
            if data_row.find("h4", string="Garage"):
                if data_row.find("h4", string="Garage").find_next_sibling().get_text() == "Yes":
                    property_data["has_garage"] = True
                if data_row.find("h4", string="Garage").find_next_sibling().get_text() == "No":
                    property_data["has_garage"] = False

            # Number Of Garages: int
            if data_row.find("h4", string="Number of garages"):
                property_data["number_of_garages"] = int(data_row.find("h4", string="Number of garages").find_next_sibling().get_text())

            # Type of Heating: str    
            if data_row.find("h4", string="Type of heating"):
                property_data["type_of_heating"] = data_row.find("h4", string="Type of heating").find_next_sibling().get_text()

            # Type of Glazing: str    
            if data_row.find("h4", string="Type of glazing"):
                property_data["type_of_glazing"] = data_row.find("h4", string="Type of glazing").find_next_sibling().get_text()

            # Specific primary energy consumption : int in  340 kWh/m²/year
            if data_row.find("h4", string="Specific primary energy consumption"):
                specific_energy_with_units = data_row.find("h4", string="Specific primary energy consumption").find_next_sibling().get_text()
                specific_eneregy_no_units = specific_energy_with_units[:-12]
                property_data["specific_primary_energy_consumption_KWh_by_m2_by_year"] = int(specific_eneregy_no_units)
                
            # Yearly total primary energy consumption : int in  44658 kWh/year
            if data_row.find("h4", string="Yearly total primary energy consumption"):
                total_primary_with_units = data_row.find("h4", string="Yearly total primary energy consumption").find_next_sibling().get_text()
                total_primary_no_units = total_primary_with_units[:-9]
                property_data["yearly_total_primary_energy_consumption_in_kWh_by_year"] = int(total_primary_no_units)
            
            # Elevator : Bool    
            if data_row.find("h4", string="Elevator"):
                if data_row.find("h4", string="Elevator").find_next_sibling().get_text() == "Yes":
                    property_data["has_elevator"] = True
                if data_row.find("h4", string="Elevator").find_next_sibling().get_text() == "No":
                    property_data["has_elevator"] = False
            
            # Access for disabled : Bool   
            if data_row.find("h4", string="Access for disabled"):
                if data_row.find("h4", string="Access for disabled").find_next_sibling().get_text() == "Yes":
                    property_data["has_access_for_disabled"] = True
                if data_row.find("h4", string="Access for disabled").find_next_sibling().get_text() == "No":
                    property_data["has_access_for_disabled"] = False

            # Low-energy house : Bool   
            if data_row.find("h4", string="Low-energy house"):
                if data_row.find("h4", string="Low-energy house").find_next_sibling().get_text() == "Yes":
                    property_data["is_low_energy"] = True
                if data_row.find("h4", string="Low-energy house").find_next_sibling().get_text() == "No":
                    property_data["is_low_energy"] = False

            # Solar panels : Bool   
            if data_row.find("h4", string="Solar panels"):
                if data_row.find("h4", string="Solar panels").find_next_sibling().get_text() == "Yes":
                    property_data["has_solar_panels"] = True
                if data_row.find("h4", string="Solar panels").find_next_sibling().get_text() == "No":
                    property_data["has_solar_panels"] = False
                    
            # Attic : Bool   
            if data_row.find("h4", string="Attic"):
                if data_row.find("h4", string="Attic").find_next_sibling().get_text() == "Yes":
                    property_data["has_attic"] = True
                if data_row.find("h4", string="Attic").find_next_sibling().get_text() == "No":
                    property_data["has_attic"] = False
                    
            # Floor heating : Bool   
            if data_row.find("h4", string="Floor heating"):
                if data_row.find("h4", string="Floor heating").find_next_sibling().get_text() == "Yes":
                    property_data["has_floor_heating"] = True
                if data_row.find("h4", string="Floor heating").find_next_sibling().get_text() == "No":
                    property_data["has_floor_heating"] = False
                    
            # Heat pump : Bool   
            if data_row.find("h4", string="Heat pump"):
                if data_row.find("h4", string="Heat pump").find_next_sibling().get_text() == "Yes":
                    property_data["has_heat_pump"] = True
                if data_row.find("h4", string="Heat pump").find_next_sibling().get_text() == "No":
                    property_data["has_heat_pump"] = False
            
            # Fireplace : Bool   
            if data_row.find("h4", string="Fireplace"):
                if data_row.find("h4", string="Fireplace").find_next_sibling().get_text() == "Yes":
                    property_data["has_fireplace"] = True
                if data_row.find("h4", string="Fireplace").find_next_sibling().get_text() == "No":
                    property_data["has_fireplace"] = False
                    
            # Balcony : Bool   
            if data_row.find("h4", string="Balcony"):
                if data_row.find("h4", string="Balcony").find_next_sibling().get_text() == "Yes":
                    property_data["has_balcony"] = True
                if data_row.find("h4", string="Balcony").find_next_sibling().get_text() == "No":
                    property_data["has_balcony"] = False



            # Build Year: int or none
            if data_row.find("h4", string="Build Year"):
                property_data["build_year"] = int(
                    data_row.find("h4", string="Build Year")
                    .find_next_sibling()
                    .get_text()
                )
            # else: property_data["build_year"] = "Unknown"

            # Terrace : True else False
            if data_row.find("h4", string="Terrace"):
                if (data_row.find("h4", string="Terrace").find_next_sibling().get_text()== "Yes"):
                    property_data["has_terrace"] = True
                if (data_row.find("h4", string="Terrace").find_next_sibling().get_text()== "No"):
                    property_data["has_terrace"] = False

            ## Terrace surface:
            if data_row.find("h4", string="Surface terrace"):
                terrace_area_with_units = (data_row.find("h4", string="Surface terrace").find_next_sibling().get_text())
                terrace_area_no_units = terrace_area_with_units[:-2]
                property_data["terrace_area_m2"] = int(terrace_area_no_units)


            # Garden : True , false or Unknown
            if data_row.find("h4", string="Garden"):
                if (data_row.find("h4", string="Garden").find_next_sibling().get_text()== "Yes"):
                    property_data["has_garden"] = True
                if (data_row.find("h4", string="Garden").find_next_sibling().get_text()== "No"):
                    property_data["has_garden"] = False



            ## Garden Surface:
            if data_row.find("h4", string="Surface garden"):
                garden_area_with_units = (data_row.find("h4", string="Surface garden").find_next_sibling().get_text())
                garden_area_no_units = garden_area_with_units[:-2]
                property_data["garden_area_m2"] = int(garden_area_no_units)


            # Total Land surface : int or unknown
            if data_row.find("h4", string="Total land surface"):
                property_area_with_units = (data_row.find("h4", string="Total land surface").find_next_sibling().get_text())
                property_area_no_units = property_area_with_units[:-2]
                property_data["land_area_m2"] = int(property_area_no_units)



            # Furnished True, False if exists, "" if unknown
            if data_row.find("h4", string="Furnished"):
                if (
                    data_row.find("h4", string="Furnished")
                    .find_next_sibling()
                    .get_text()
                    == "Yes"
                ):
                    property_data["furnished"] = True
                else:
                    property_data["furnished"] = False
            # else: property_data["Furnished"] = ""

            # Facades: int
            if data_row.find("h4", string="Number of facades"):
                property_data["number_of_facades"] = int(
                    data_row.find("h4", string="Number of facades")
                    .find_next_sibling()
                    .get_text()
                )

            # Swimming pool: True Or False
            if data_row.find("h4", string="Swimming pool"):
                if (
                    data_row.find("h4", string="Swimming pool")
                    .find_next_sibling()
                    .get_text()
                    == "Yes"
                ):
                    property_data["has_swimming_pool"] = True
                else:
                    property_data["has_swimming_pool"] = False

            # Kitchen Equipment:
            if data_row.find("h4", string="Kitchen equipment"):
                property_data["kitchen_equipment"] = (
                    data_row.find("h4", string="Kitchen equipment")
                    .find_next_sibling()
                    .get_text()
                )

            # Number of bedrooms:
            if data_row.find("h4", string="Number of bedrooms"):
                property_data["number_of_bedrooms"] = int(data_row.find("h4", string="Number of bedrooms").find_next_sibling().get_text())

        # .find_next_sibling().get_text()

        ## Magic block has a lot of stuff:
        for magicbox in soup.find_all("script", type="text/javascript"):
            magic_text = magicbox.get_text()
            magic_block = re.search(
                r"dataLayer\.push\(\s*(\{[^}]*\})\s*\|\|", magic_text, re.S
            )
            if magic_block:
                try:
                    magic_data = json.loads(magic_block.group(1))
                    property_data["price"] = int(float(magic_data.get("price")))
                    property_data["property_type"] = magic_data.get("property_type")
                    property_data["property_subtype"] = magic_data.get(
                        "property_sub_type"
                    )
                    property_data["livable_surface_m2"] = int(
                        float(magic_data.get("livable_surface"))
                    )
                    property_data["zip_code"] = int(magic_data.get("zip_code"))
                except:
                    pass
                break

        append_dict_jsonl(property_data, target_path)

    except Exception as e:
        print("errore su {} : {}".format(url, e))
        return None

    return property_data





##
### Calling the functions for testing
##
url = "https://immovlan.be/en/detail/residence/for-sale/6200/chatelet/vbd89512"

with requests.Session() as session:
    improved_scrape_data_from_property_page(url, 1, session, "improving_scrape_a_page_tests.jsonl")


## This, chat told me to implement so the function doesn't trigger on import
""" 
if __name__ == "__main__":
    url = "https://immovlan.be/en/detail/ground-floor/for-sale/1050/elsene/vbd49955"
    scrape_data_from_property_page(
        url, page_index=1, session=None, target_path="testing_scrape_a_page.jsonl"
    )
    
 """