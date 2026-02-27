import pandas as pd
import json
import numpy as np


def clean_text(valore):
    # Se il valore è una stringa, togliamo gli spazi ai lati
    if isinstance(valore, str):
        return valore.strip()
    # Se non è una stringa (es. è un numero o None), restituiscilo così com'è
    return valore


def clean_to_numerical_absolute_na(input_file, output_csv):
    data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))

    df = pd.DataFrame(data)

    # --- STEP 0: RIMOZIONE DUPLICATI ---
    if "page_url" in df.columns:
        # Teniamo la prima occorrenza (keep='first') e rimuoviamo le altre
        conteggio_iniziale = len(df)
        df = df.drop_duplicates(subset=["page_url"], keep="first")
        duplicati_rimossi = conteggio_iniziale - len(df)
        if duplicati_rimossi > 0:
            print(f"🧹 Pulizia: rimossi {duplicati_rimossi} URL duplicati.")

    # --- STEP 1: PULIZIA AGGRESSIVA DEI VUOTI ---

    # Invece della lambda, usiamo la funzione definita sopra
    df = df.map(clean_text)

    # Sostituiamo le stringhe vuote o di soli spazi con NaN (Not a Number)
    df = df.replace(r"^\s*$", np.nan, regex=True)

    # Sostituiamo la parola "None" scritta come testo con il valore nullo reale
    df = df.replace("None", np.nan)

    # --- STEP 2: GESTIONE BINARIA (1, 0) ---
    binary_cols = ["furnished", "has_terrace", "has_garden", "has_swimming_pool"]

    # Creiamo un dizionario di mappatura chiaro
    binary_map = {True: 1, False: 0, 1: 1, 0: 0, "1": 1, "0": 0}

    for col in binary_cols:
        if col in df.columns:
            # Usiamo il dizionario per convertire i valori
            df[col] = df[col].map(binary_map)

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
            # Nuova Regex: r"(\d+[.,]?\d*)" -> prende 16,5 o 16.5
            df[col] = df[col].astype(str).str.extract(r"(\d+[.,]?\d*)")
            # Passaggio extra: standardizzare la virgola in punto
            df[col] = df[col].str.replace(",", ".")
            # Infine convertiamo in numero
            df[col] = df[col].astype(float)

    # --- STEP 4: SALVATAGGIO ---
    df["page_id"] = pd.to_numeric(df["page_id"], errors="coerce")
    df.sort_values(by="page_id", inplace=True)

    # Salvataggio con l'etichetta N/A per i campi vuoti
    df.to_csv(output_csv, index=False, na_rep="N/A", encoding="utf-8")

    print(f" CSV generato. Ora ogni cella vuota è riempita con 'N/A'")


# Esegui
clean_to_numerical_absolute_na("4.projects_output.jsonl", "database_projects.csv")
