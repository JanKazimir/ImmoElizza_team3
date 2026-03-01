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
from improved_scrape_a_property import improved_scrape_data_from_property_page





def open_json_and_put_links_in_dict(source_file):
    with open(source_file, "r") as f:
        data = json.load(f)
        links_as_dict = {}

        for item in data:
            links_as_dict[item["id"]] = item["url"]
    return links_as_dict



def simpler_scrape_all_property_pages_with_index(source_file, target_path, clean_data_path):
    # THis function scrape all property pages from a list of dictionaries
    start_time = datetime.now()
    print(f"starting at: {start_time}")
 

    links_as_dict = open_json_and_put_links_in_dict(source_file)
    links_as_dict = open_json_and_put_links_in_dict(source_file)
    all_links = list(links_as_dict.items())
    start_index = 0
    links_rimanenti = all_links[start_index:]

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(
                     improved_scrape_data_from_property_page,
                     [link[1] for link in links_rimanenti],
                     [link[0] for link in links_rimanenti],
                     [session] * len(links_rimanenti),
                     [target_path] * len(links_rimanenti),)
            
            with open(clean_data_path, "a", encoding="utf-8") as f:
                for i, result in enumerate(results, 1):
                    if result:
                        print(f" Scraping page: {i}", end="\r")
                        f.write(json.dumps(result, ensure_ascii=False) + "\n")
                
    finished_time = datetime.now()
    print(f"finished at: {finished_time}. Total time: {finished_time - start_time}")

#simpler_scrape_all_property_pages_with_index("data/input_files/200_links_for_testing.json", "test_for_simplerprint.jsonl", "testing new stuff.jsonl")



## this was made with ai. It works, but the resulting file is disorderly. 
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
    start_index = 0
    links_rimanenti = all_links[start_index:]

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(improved_scrape_data_from_property_page, link[1], link[0], session, target_path)
                for link in links_rimanenti
            ]
            property_data = []
            for i, future in enumerate(futures, 1):
                try:
                    result = future.result(timeout=30)
                    print(f"Scraped {i}/{len(links_rimanenti)}", end="\r")
                    property_data.append(result)
                except Exception as e:
                    print(f"Error on item {i + start_index}: {e}")
                    property_data.append(None)
        for item in property_data:
            if item:
                final_list.append(item)

    print("finished at:")
    print(datetime.now())
 
#scrape_all_property_pages_from_index("input_files/all_links_thursday_two_twenty.json", "all_properties_improved_data_collector.jsonl")


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
                    improved_scrape_data_from_property_page,
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











#scrape_all_property_pages("", "")

# --- Original version of scrape_all_property_pages_from_index (before progress print) ---
# def scrape_all_property_pages_from_index(source_file, target_path):
#     print("starting at:")
#     print(datetime.now())
#     final_list = []
#     links_as_dict = open_json_and_put_links_in_dict(source_file)
#     all_links = list(links_as_dict.items())
#     start_index = 1
#     links_rimanenti = all_links[start_index:]
#
#     with requests.Session() as session:
#         with ThreadPoolExecutor(max_workers=10) as executor:
#             property_data = list(
#                 executor.map(
#                     improved_scrape_data_from_property_page,
#                     [link[1] for link in links_rimanenti],
#                     [link[0] for link in links_rimanenti],
#                     [session] * len(links_rimanenti),
#                     [target_path] * len(links_rimanenti),
#                 )
#             )
#         for item in property_data:
#             if item:
#                 final_list.append(item)
#
#     print("finished at:")
#     print(datetime.now())


