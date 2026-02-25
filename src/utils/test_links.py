from .link_manager import save_unique_links

links = [
    "https://immovlan.be/en/detail/duplex/for-sale/5000/namur/vbd84195",
    "https://immovlan.be/en/detail/residence/for-sale/5000/namur/vbd90542",
    "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd90186",
    "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89975",
    "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89364",
    
]

unique, dupes = save_unique_links(links)

print("Unique ones:", unique)
print("Duplicate ones:", dupes)