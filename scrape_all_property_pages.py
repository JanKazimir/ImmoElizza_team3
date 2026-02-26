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
# create a session and pass that to the scrape data

## What we need to give : a url, a target file, a page index, and a session (to be implemented)

# let's do the easy thing: make a list of three urls, and get that to work with a session

# Add exception handling


def scrape_all_property_pages(target_path="testing_scrape_a_page.jsonl"):
    ## here we get the list
    
    test_prop_links_list = ["https://immovlan.be/en/detail/apartment/for-sale/1050/elsene/vbd91331", "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89112", "https://immovlan.be/en/detail/residence/for-sale/4000/liege/vbd90637"]
    target_path= target_path
    
    # to work from a list. 
    for index, url in enumerate(test_prop_links_list, start=1):
        url = url
        page_index = index
        with requests.Session() as session:
            scrape_data_from_property_page(url, page_index, session, target_path)


scrape_all_property_pages()

## testing quick: works
#url = "https://immovlan.be/en/detail/residence/for-sale/2970/schilde/rbv23379"
#scrape_data_from_property_page(url)
