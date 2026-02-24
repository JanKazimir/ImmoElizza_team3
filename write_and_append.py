import csv
links_as_dict = {'4': ['https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd86951', 'https://immovlan.be/en/detail/villa/for-sale/1000/brussels/rbv09716', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd90215', 'https://immovlan.be/en/detail/studio/for-sale/1000/brussels/vbd90167', 'https://immovlan.be/en/detail/ground-floor/for-sale/1000/brussels/vbd90166', 'https://immovlan.be/en/detail/loft/for-sale/1000/brussels/vbd90160', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd89713', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/rbv33376', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd89582', 'https://immovlan.be/en/detail/penthouse/for-sale/1000/brussels/vbd89485', 'https://immovlan.be/en/detail/master-house/for-sale/1000/brussels/vbd89465', 'https://immovlan.be/en/detail/studio/for-sale/1000/brussels/vbd89451', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd89450']}

## Not sure about this: 
### we should also write a url id, in case we need it for the loops       
def write_links_to_file(links_as_dict):
    with open("test_links.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames= ["page_number", "url"]
        writer = csv.writer(f)
        writer.writerow(["page_number", "url"])
        
        for page_number, links in links_as_dict.items():
            for url in links:
                writer.writerow([page_number, url])


        
#write_links_to_file(links_as_dict)        
        
def append_links_to_file(links_as_dict):
    with open("test_links.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        #writer.writerow(["page_number", "url"])
        
        for page_number, links in links_as_dict.items():
            for url in links:
                writer.writerow([page_number, url])     
 
just_in_case_links = ['https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd86951', 'https://immovlan.be/en/detail/villa/for-sale/1000/brussels/rbv09716', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd90215', 'https://immovlan.be/en/detail/studio/for-sale/1000/brussels/vbd90167', 'https://immovlan.be/en/detail/ground-floor/for-sale/1000/brussels/vbd90166', 'https://immovlan.be/en/detail/loft/for-sale/1000/brussels/vbd90160', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd89713', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/rbv33376', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd89582', 'https://immovlan.be/en/detail/penthouse/for-sale/1000/brussels/vbd89485', 'https://immovlan.be/en/detail/master-house/for-sale/1000/brussels/vbd89465', 'https://immovlan.be/en/detail/studio/for-sale/1000/brussels/vbd89451', 'https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/vbd89450']

write_links_to_file(links_as_dict)
append_links_to_file(links_as_dict)


#write_links_to_file(just_in_case_links)

    