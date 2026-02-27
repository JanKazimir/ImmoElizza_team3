# Imports
import re
import requests
from bs4 import BeautifulSoup
import time
import csv
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

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
            links_as_dict[item["id"]] = item["url"]
    return links_as_dict


def scrape_all_property_pages_from_index(source_file, target_path):
    # THis function scrape all property pages from a list of dictionaries, and start form start_index (set it inside de function)

    ## here we get the list
    print("starting at:")
    print(datetime.now())
    final_list = []
    # list_of_links = ["https://immovlan.be/en/detail/apartment/for-sale/1050/elsene/vbd91331", "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89112", "https://immovlan.be/en/detail/residence/for-sale/4000/liege/vbd90637"]

    links_as_dict = open_json_and_put_links_in_dict(source_file)
    # print(links_as_dict)
    all_links = list(links_as_dict.items())
    start_index = 22500
    links_rimanenti = all_links[start_index:]

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            property_data = list(
                executor.map(
                    scrape_data_from_property_page,
                    [link[1] for link in links_rimanenti],
                    [link[0] for link in links_rimanenti],
                    [session] * len(links_rimanenti),
                    [target_path] * len(links_rimanenti),
                )
            )
        for item in property_data:
            if item:
                final_list.append(item)

    print("finished at:")
    print(datetime.now())


def scrape_all_property_pages(source_file, target_path):
    # THis function scrape all property pages from a list of dictionaries

    print("starting at:")
    print(datetime.now())

    final_list = []
    links_as_dict = open_json_and_put_links_in_dict(source_file)

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            property_data = list(
                executor.map(
                    scrape_data_from_property_page,
                    links_as_dict.values(),
                    links_as_dict.keys(),
                    [session] * len(links_as_dict),
                    [target_path] * len(links_as_dict),
                )
            )
        for item in property_data:
            if item:
                final_list.append(item)

    print("finished at:")
    print(datetime.now())


scrape_all_property_pages("single_project_links.json", "4.projects_output.jsonl")

# scrape_all_property_pages_from_index("links.json", "3.output.jsonl")

## testing quick: works
# url = "https://immovlan.be/en/detail/residence/for-sale/2970/schilde/rbv23379"
# scrape_data_from_property_page(url)


"""
def scrape_all_property_pages(source_file, target_path):
    ## whitout the multithread
    print("starting at:")
    print(datetime.now())
    #list_of_links = ["https://immovlan.be/en/detail/apartment/for-sale/1050/elsene/vbd91331", "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89112", "https://immovlan.be/en/detail/residence/for-sale/4000/liege/vbd90637"]
    
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
"""
