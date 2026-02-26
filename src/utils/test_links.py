from link_manager import save_links_by_city

# Sample mixed-city property links for testing
links = [
    "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89364",
    "https://immovlan.be/en/detail/apartment/for-sale/2000/antwerp/abc123",
    "https://immovlan.be/en/detail/apartment/for-sale/1000/brussels/xyz999",
    "https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89364",  # duplicate test
]

# Call the function to save links grouped by city
results = save_links_by_city(links)

# Step 4: Print detailed debug info for each city
for city, data in results.items():
    print(f"\nCity: {city}")
    print(f"  New links added: {len(data['unique'])}")
    print(f"  Duplicates skipped: {len(data['duplicates'])}")
    if data['unique']:
        print(f"    Unique links: {data['unique']}")
    if data['duplicates']:
        print(f"    Duplicates: {data['duplicates']}")