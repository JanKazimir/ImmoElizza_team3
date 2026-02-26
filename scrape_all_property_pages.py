# Imports
import re
import requests
from bs4 import BeautifulSoup
import time
import csv
import json
## Importing files
from scrape_a_property_page import scrape_data_from_property_page



## This is where we write the funciton that call on  scrape_data_from_property_page() to scrape all the page:
# What we need to do 
# we get a list. either as a csv or as a list. 

# let's do the easy thing: make a list of three urls, and get that to work with a session

# Add exception handling

# scrape_data_from_property_page needs: (url, page_index, session, target_path)

def open_json_and_put_links_in_dict(source_file):
    with open(source_file, "r") as f:
        data = json.load(f)
        links_as_dict = {}
        
        for item in data:
            links_as_dict[item["id"]] = links_as_dict["id"]
            links_as_dict[item['url']] = item['url']
    print(links_as_dict)        
    return links_as_dict
        



def scrape_all_property_pages(source_file="links_for_jan_test.json", target_path="testing_scrape_a_page.jsonl"):
    ## here we get the list
    source_file = "links_for_jan_test.json"
    list_of_links = ["https://immovlan.be/en/detail/apartment/for-sale/1050/elsene/vbd91331", "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89112", "https://immovlan.be/en/detail/residence/for-sale/4000/liege/vbd90637"]
    
    links_as_dict = open_json_and_put_links_in_dict(source_file)
    print(links_as_dict)
    
    for index, url in links_as_dict.items():
        print(index, url)
        
        with requests.Session() as session:
            time.sleep(0.1)
            print("waiting a bit...")
            try:
                scrape_data_from_property_page(url, index, session, target_path)
            except Exception as e:
                print(f"Got an error:{e}  on index {index}, continuing...")
                continue
        
""" 
    # We scrape all the links from a list:
    for index, url in enumerate(list_of_links, start=1):
        pass
        url = url
        url_index = index
        with requests.Session() as session:
            time.sleep(0.1)
            print("waiting a bit...")
            try:
                scrape_data_from_property_page(url, url_index, session, target_path)
            except Exception as e:
                print(f"Got an error:{e}  on index {index}, continuing...")
                continue
   """          
    


scrape_all_property_pages()

## testing quick: works
#url = "https://immovlan.be/en/detail/residence/for-sale/2970/schilde/rbv23379"
#scrape_data_from_property_page(url)

""" 
            print(
                f"Scaricando pagina {n}...", end="\r"
            )  # end='\r' sovrascrive la stessa riga, molto pulito!
            
             """