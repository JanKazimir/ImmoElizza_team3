import pandas as pd
import json
import numpy as np


def clean_to_numerical_absolute_na(input_file, output_csv):
    data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

    df = pd.DataFrame(data)

    # --- STEP 1: PULIZIA AGGRESSIVA DEI VUOTI ---
    # Rimuove spazi bianchi dalle stringhe e trasforma le stringhe vuote "" in veri NaN
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.replace(r"^\s*$", np.nan, regex=True)
    df = df.replace("None", np.nan)  # Gestisce eventuali stringhe "None" letterali

    # --- STEP 2: GESTIONE BINARIA (1, 0) ---
    binary_cols = ["furnished", "has_terrace", "has_garden", "has_swimming_pool"]
    for col in binary_cols:
        if col in df.columns:
            # Mappiamo esplicitamente, i mancanti restano NaN
            df[col] = df[col].map({True: 1, False: 0, 1: 1, 0: 0, "1": 1, "0": 0})

    # --- STEP 3: PULIZIA STRINGHE NUMERICHE ---
    cols_to_numeric = [
        "terrace_area_m2",
        "garden_area_m2",
        "land_area_m2",
        "livable_surface_m2",
        "price",
        "number_of_bedrooms",
    ]
    for col in cols_to_numeric:
        if col in df.columns:
            # Estraiamo i numeri e forziamo a float (che supporta i NaN)
            df[col] = df[col].astype(str).str.extract(r"(\d+)").astype(float)

    # --- STEP 4: SALVATAGGIO ---
    # Ordinamento
    df["page_id"] = pd.to_numeric(df["page_id"], errors="coerce")
    df.sort_values(by="page_id", inplace=True)

    # Salvataggio: na_rep forzerà la scritta N/A su ogni singola cella vuota (NaN)
    df.to_csv(output_csv, index=False, na_rep="N/A", encoding="utf-8")

    print(f"✅ CSV generato. Ora ogni cella vuota è riempita con 'N/A'")


# Esegui
clean_to_numerical_absolute_na("3.output.jsonl", "database_senza_vuoti.csv")
