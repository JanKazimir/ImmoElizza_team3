import csv
from pathlib import Path
from urllib.parse import urlparse

def get_city_from_url(link: str) -> str:
    """Extract the city slug from the Immovlan property URL"""
    parts = urlparse(link).path.split("/")
    return parts[6].lower()  # 7. segment is city

def save_properties_by_city(property_list, base_folder="properties_by_city"):
    """
    Save full property dicts into separate CSV files per city.
    Each CSV contains: id, zip, url
    """
    base_path = Path(base_folder)
    base_path.mkdir(exist_ok=True)

    city_groups = {}

    # Group properties by city
    for prop in property_list:
        link = prop["url"]
        city = get_city_from_url(link)

        if city not in city_groups:
            city_groups[city] = []
        city_groups[city].append(prop)

    results = {}

    # Process each city
    for city, props in city_groups.items():
        csv_path = base_path / f"{city}_properties.csv"

        # Load existing URLs to avoid duplicates
        if csv_path.exists():
            with open(csv_path, "r", newline="", encoding="utf-8") as f:
                existing_urls = {row[2] for row in csv.reader(f)}  # url is third column
        else:
            existing_urls = set()

        unique_props = []
        duplicates = []

        for prop in props:
            if prop["url"] not in existing_urls:
                unique_props.append(prop)
            else:
                duplicates.append(prop)

        # Write unique properties
        if unique_props:
            with open(csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # write header if file is new
                if f.tell() == 0:
                    writer.writerow(["id", "zip", "url"])
                for prop in unique_props:
                    writer.writerow([prop["id"], prop["zip"], prop["url"]])

        results[city] = {
            "unique": unique_props,
            "duplicates": duplicates
        }

    return results