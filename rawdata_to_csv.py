import pandas as pd
import json


def process_scraped_data(input_file, output_csv):

    data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # Salta righe malformate se presenti

    # Creiamo un DataFrame (la "tabella" di Pandas)
    df = pd.DataFrame(data)

    initial_count = len(df)
    df = df.drop_duplicates(subset=["page_url"], keep="first")
    final_count = len(df)
    print(f"Rimossi {initial_count - final_count} duplicati.")

    df["page_id"] = pd.to_numeric(df["page_id"])
    df = df.sort_values(by="page_id")
    print("✅ Dati ordinati per page_id.")

    df.to_csv(output_csv, index=False, na_rep="N/A", encoding="utf-8")
    print(f"File CSV salvato con successo: {output_csv}")
    print(f"Totale record unici: {len(df)}")


process_scraped_data("3.output.jsonl", "final_properties_data.csv")
