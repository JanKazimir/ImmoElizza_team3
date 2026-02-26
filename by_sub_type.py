import pandas as pd
import os


def split_csv_by_property_type(input_csv, output_folder="split_data"):
    # Carichiamo il CSV appena creato (quello già pulito con i N/A)
    # Importante: keep_default_na=False e na_values=['N/A'] serve a Pandas
    # per riconoscere correttamente i tuoi N/A personalizzati
    df = pd.read_csv(input_csv, na_values=["N/A"], keep_default_na=False)

    # Creiamo la cartella di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"📁 Cartella '{output_folder}' creata.")

    # Troviamo tutti i tipi di proprietà unici
    property_types = df["property_type"].dropna().unique()

    print(f"🔍 Trovati {len(property_types)} tipi di proprietà. Inizio la divisione...")

    for p_type in property_types:
        # Filtriamo il dataframe per il tipo specifico
        # Puliamo il nome per evitare problemi con i caratteri speciali nei nomi dei file
        clean_name = str(p_type).lower().replace(" ", "_").replace("/", "_")

        subset = df[df["property_type"] == p_type]

        # Nome del file finale
        output_filename = os.path.join(output_folder, f"properties_{clean_name}.csv")

        # Salviamo il subset mantenendo la coerenza dei N/A
        subset.to_csv(output_filename, index=False, na_rep="N/A", encoding="utf-8")

        print(f"  - Generato: {output_filename} ({len(subset)} righe)")

    print("\n✅ Suddivisione completata con successo!")


# Esempio di utilizzo:
split_csv_by_property_type("database_senza_vuoti.csv")
