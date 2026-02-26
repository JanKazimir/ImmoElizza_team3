import csv
from pathlib import Path
from urllib.parse import urlparse

def get_city_from_url(link: str) -> str:
    """
    Extract the city slug from the Immovlan property URL.

    Example URL:
    https://immovlan.be/en/detail/apartment/for-sale/5000/namur/vbd89364

    Breakdown:
        - 5000 -> postal code
        - namur -> city
        - vbd89364 -> property ID

    Why we do this:
        - We want to store properties by city so datasets don't mix.
        - Using the URL is faster than scraping each property page.
        - We convert to lowercase to normalize filenames.
    """
    parts = urlparse(link).path.split("/")
    return parts[6].lower()  # pick the 7th part (0-indexed)

def save_links_by_city(new_links, base_folder="links_by_city"):
    """
    Save incoming property links into separate CSV files based on city.

    How it works:
        1. Group all incoming links by city.
        2. For each city, check the CSV file (if exists) to avoid duplicates.
        3. Append only new links to the respective city's CSV file.
        4. Return a results dictionary for logging and testing.

    Why we do each step:
        - Grouping first reduces file I/O, making the process faster for many links.
        - Duplicate checking ensures we don't scrape the same property twice.
        - Separate CSV per city keeps datasets clean for ML, analysis, or export.
    """

    base_path = Path(base_folder)
    base_path.mkdir(exist_ok=True)  # create main folder if it doesn't exist

    city_groups = {}  # dictionary to group links by city before saving

    # Step 1: Group links by city
    for link in new_links:
        city = get_city_from_url(link)  # extract city slug

        if city not in city_groups:
            city_groups[city] = []  # initialize list for new city

        city_groups[city].append(link)  # add link to its city group

    results = {}  # dictionary to keep track of unique and duplicate links per city

    # Step 2: Process each city's links
    for city, links in city_groups.items():

        csv_path = base_path / f"{city}_links.csv"  # each city gets its own CSV

        # Step 2a: Load existing links for duplicate checking
        if csv_path.exists():
            with open(csv_path, "r", newline="", encoding="utf-8") as f:
                existing_links = {row[0] for row in csv.reader(f)}
                # using a set for O(1) lookup, very fast even for thousands of links
        else:
            existing_links = set()  # start with empty set if file does not exist

        unique_links = []  # will store links that are new for this city
        duplicates = []    # will store links already saved

        # Step 2b: Separate incoming links into unique vs duplicate
        for link in links:
            if link not in existing_links:
                unique_links.append(link)  # new link, save it later
            else:
                duplicates.append(link)    # already saved, skip

        # Step 2c: Append only the new links to the CSV
        if unique_links:
            with open(csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                for link in unique_links:
                    writer.writerow([link])  # one link per row
                    # Why not write duplicates? Because we already stored them before

        # Step 2d: Keep a result summary for logging/testing purposes
        results[city] = {
            "unique": unique_links,
            "duplicates": duplicates
        }

    # Step 3: Return results so user can see what was added and skipped
    return results