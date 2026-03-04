# Imports
import re
import requests
from bs4 import BeautifulSoup
import time
import csv
import json
from datetime import datetime
## ❗ Importing files files will have moved in the big reorganising.
from scrape_a_property_page_backup import scrape_data_from_property_page



## This is where we write the funciton that call on  scrape_data_from_property_page() to scrape all the page:

def open_json_and_put_links_in_dict(source_file):
    with open(source_file, "r") as f:
        data = json.load(f)
        links_as_dict = {}
        
        for item in data:
            links_as_dict[item["id"]] = item['url']   
    return links_as_dict
        


# this call a function to scrape property data, on a source file or urls and writes it to an output file. 
def scrape_all_property_pages(source_file, target_path):
    ## here we get the list
    print("starting at:")
    print(datetime.now())
    list_of_links = ["https://immovlan.be/en/detail/apartment/for-sale/1050/elsene/vbd91331", "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89112", "https://immovlan.be/en/detail/residence/for-sale/4000/liege/vbd90637"]
    
    links_as_dict = open_json_and_put_links_in_dict(source_file)
    #print(links_as_dict)
    with requests.Session() as session:
        for index, url in links_as_dict.items():
        
            time.sleep(0.1)
            print(f"Scaricando pagina {index}...", end="\r")
            try:
                scrape_data_from_property_page(url, index, session, target_path)
            except Exception as e:
                print(f"Got an error:{e}  on index {index}, continuing...")
                continue
    print("finished at:")
    print(datetime.now())        


 
#scrape_all_property_pages("200_links_for_testing.json","200_links_output.jsonl" ) 
 
