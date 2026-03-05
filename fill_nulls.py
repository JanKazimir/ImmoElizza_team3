"""
Fill null fields in property JSONL using a local LLM via Ollama.

Well, it's a complete disaster. not only is it slow as shit, like twenty seconds per line, but it's adding nulls. Adding them! what a giant stupid waste of time.

Usage:
    1. Make sure Ollama is running (`ollama serve`)
    2. Pull a model (`ollama pull mistral`)
    3. python fill_nulls.py
"""

import json
import random
import time
import ollama

# ── Config ───────────────────────────────────────────────────────────────
INPUT_FILE =  'aajan_stuff/data/output_files/all_properties_data_improved_backup.jsonl'   #"properties.jsonl"
OUTPUT_FILE = "aajan_stuff/data/output_files/properties_llm_filled.jsonl"
MODEL = "llama3.2:1b"            # try: mistral, phi3, llama3.2
BATCH_SIZE = 50              # set to None to process all rows

# ── Prompt options (uncomment the one you want) ────────────────────────

# Option A: Conservative — only fill from explicit mentions in description
PROMPT = """You are a data-cleaning assistant for Belgian real estate listings.

Given the JSON record below, fill in null fields ONLY if the property description 
explicitly mentions the information. Do NOT guess or infer. If in doubt, leave it as it is.

Return the complete JSON record with nulls replaced where possible.
Return ONLY valid JSON, nothing else."""

# # Option B: Moderate — fill from description + correct obvious errors
#PROMPT = """You are a data-cleaning assistant for Belgian real estate listings.
#
# Given the JSON record below:
# 1. Fill in null fields if the description explicitly or strongly implies the information.
# 2. If an existing non-null value clearly contradicts the description, correct it.
# 3. When unsure, leave the value as-is.
#
# Return the complete JSON record with updates applied.
# Return ONLY valid JSON, nothing else."""

# # Option C: Aggressive — fill + infer from context
# PROMPT = """You are a data-cleaning assistant for Belgian real estate listings.
#
# Given the JSON record below:
# 1. Fill in null fields from the description (explicit or implied).
# 2. Correct existing values that contradict the description.
# 3. For boolean fields (has_garden, has_cellar, etc.), infer from context if reasonable.
#    For example, if garden_area_m2 is set, has_garden should be true.
# 4. When unsure, leave the value as-is.
#
# Return the complete JSON record with updates applied.
# Return ONLY valid JSON, nothing else."""


def fill_row(row: dict) -> dict:
    """Send one row to Ollama, get back the filled version."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": json.dumps(row)},
        ],
        format="json",
    )
    return json.loads(response["message"]["content"])


def main():
    # Load
    with open(INPUT_FILE) as f:
        rows = [json.loads(line) for line in f if line.strip()]

    print(f"Loaded {len(rows)} rows from {INPUT_FILE}")

    # Shuffle (comment out to keep original order)
    # random.shuffle(rows)

    # Slice for testing (set BATCH_SIZE = None to run all)
    batch = rows[:BATCH_SIZE] if BATCH_SIZE else rows
    print(f"Processing {len(batch)} rows with model '{MODEL}'...\n")

    with open(OUTPUT_FILE, "w") as out:
        for i, row in enumerate(batch):
            t0 = time.time()
            try:
                filled = fill_row(row)
                out.write(json.dumps(filled) + "\n")
                elapsed = time.time() - t0
                # Quick summary of what changed
                nulls_before = sum(1 for v in row.values() if v is None)
                nulls_after = sum(1 for v in filled.values() if v is None)
                print(f"  [{i+1}/{len(batch)}] page_id={row.get('page_id')} "
                      f"nulls: {nulls_before} → {nulls_after}  ({elapsed:.1f}s)")
            except Exception as e:
                # On error, write original row unchanged
                out.write(json.dumps(row) + "\n")
                print(f"  [{i+1}/{len(batch)}] page_id={row.get('page_id')} ERROR: {e}")

    print(f"\nDone. Output written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
