import csv
import json


# This is for all file handling functions:


## Let's create a function to turn a jsonl to a csv.

# output_file_path
def turn_a_jsonl_to_csv(input_file_path, output_file_path):
    with open(input_file_path, "r") as input_file:
        rows = [json.loads(line) for line in input_file if line.strip()]
    

    with open(output_file_path, "w", newline="") as output_file:
        fieldnames = rows[0].keys()   
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
                    



turn_a_jsonl_to_csv("output files/all_property_data_jan_thursday_scrape.jsonl", "all_property_data_jan_thursday_scrape.csv")

    