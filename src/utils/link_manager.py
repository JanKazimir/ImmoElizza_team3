import csv
from pathlib import Path

def save_unique_links(new_links, csv_path="links.csv"):
    csv_file = Path(csv_path)

    # Daha önce kaydedilen linkleri oku
    if csv_file.exists():
        with open(csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            existing_links = {row[0] for row in reader}
    else:
        existing_links = set()

    unique_links = []
    duplicates = []

    for link in new_links:
        if link not in existing_links:
            unique_links.append(link)
        else:
            duplicates.append(link)

    # CSV’ye sadece yeni olanları ekle
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for link in unique_links:
            writer.writerow([link])

    return unique_links, duplicates