import csv
import json

            # -----------------------------------------------------#
            #       This is for all file handling functions        #
            # =====================================================#




## Function to turn a jsonl to a csv.
def turn_a_jsonl_to_csv(input_file_path, output_file_path):
    with open(input_file_path, "r") as input_file:
        rows = [json.loads(line) for line in input_file if line.strip()]
    

    with open(output_file_path, "w", newline="") as output_file:
        fieldnames = rows[0].keys()   
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
                    



# takes a dict, write it to a csv ❗ needs modification for using      
def write_links_to_file(links_as_dict):
    with open("test_links.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames= ["page_number", "url"]
        writer = csv.writer(f)
        writer.writerow(["page_number", "url"])
        
        for page_number, links in links_as_dict.items():
            for url in links:
                writer.writerow([page_number, url])




# Takes a dict, appends it to a csv ❗ needs modifying to use.
def append_links_to_file(links_as_dict):
    with open("test_links.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        #writer.writerow(["page_number", "url"])
        
        for page_number, links in links_as_dict.items():
            for url in links:
                writer.writerow([page_number, url])     