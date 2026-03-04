import csv
from pathlib import Path


def merge_all_city_csvs_unique(
    source_folder="properties_by_city",
    output_file="ALL_PROPERTIES_UNIQUE.csv"
):
    source_path = Path(source_folder)

    if not source_path.exists():
        print("❌ Folder not found:", source_path.resolve())
        return

    csv_files = list(source_path.glob("*_properties.csv"))

    if not csv_files:
        print("❌ No CSV files found.")
        return

    print(f"📦 {len(csv_files)} CSV Found, merge starts...\n")

    seen_urls = set()
    all_rows = []
    header = None

    for file in csv_files:
        print("➡️ Okunuyor:", file.name)

        with open(file, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            try:
                file_header = next(reader)
            except StopIteration:
                continue

            if header is None:
                header = file_header

            for row in reader:
                url = row[2]

                if url not in seen_urls:
                    seen_urls.add(url)
                    all_rows.append(row)

    output_path = Path(output_file)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(all_rows)

    print("\n✅ DONE")
    print("📄 ALL Unique records:", len(all_rows))
    print("💾 File:", output_path.resolve())


if __name__ == "__main__":
    merge_all_city_csvs_unique()