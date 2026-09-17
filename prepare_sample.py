import pandas as pd
import json
import os
import re

PARQUET_FILE = "enwiki_namespace_0_00001.parquet"
OUTPUT_JSONL = "sample_wiki.jsonl"

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Replace unicode dashes, quotes, and replacement characters with standard ASCII equivalents
    text = text.replace('\u2013', '-').replace('\u2014', '-').replace('\ufffd', '-')
    text = text.replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    # Remove hidden control characters
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text).strip()

def clean_obj(obj):
    if isinstance(obj, str):
        return clean_text(obj)
    elif isinstance(obj, list):
        return [clean_obj(item) for item in obj]
    elif isinstance(obj, dict):
        return {clean_text(k): clean_obj(v) for k, v in obj.items()}
    return obj

def prepare_sample_jsonl():
    if not os.path.exists(PARQUET_FILE):
        print(f"Error: {PARQUET_FILE} not found.")
        return

    print(f"Loading dataset from {PARQUET_FILE}...")
    df = pd.read_parquet(PARQUET_FILE)

    samples = []
    count = 0
    target_count = 200

    for idx, row in df.iterrows():
        name = row['name']
        abstract = row['abstract']
        infoboxes_raw = row['infoboxes']

        if not name or not abstract or len(str(abstract).strip()) < 50:
            continue
        
        if not infoboxes_raw or infoboxes_raw == '[]':
            continue

        try:
            parsed_infoboxes = json.loads(infoboxes_raw)
            if not parsed_infoboxes or len(parsed_infoboxes) == 0:
                continue

            clean_name = clean_text(name)
            clean_abstract = clean_text(abstract)
            clean_infoboxes = clean_obj(parsed_infoboxes)

            samples.append({
                "name": clean_name,
                "abstract": clean_abstract,
                "infoboxes": clean_infoboxes
            })

            count += 1
            if count >= target_count:
                break
        except Exception as e:
            continue

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for item in samples:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Successfully created {OUTPUT_JSONL} with {len(samples)} articles.")

if __name__ == "__main__":
    prepare_sample_jsonl()
