import os
import spacy
import requests
import pandas as pd
from collections import Counter
from nltk.tokenize import sent_tokenize
from utils.pdf_utils import extract_text_without_references

nlp = spacy.load("en_core_sci_md")

def is_valid_species_gbif(name):
    try:
        response = requests.get(
            "https://api.gbif.org/v1/species/match",
            params={"name": name},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("matchType") == "EXACT" and data.get("rank") == "SPECIES"
        return False
    except Exception as e:
        print(f"GBIF error for '{name}': {e}")
        return False

def extract_species_from_pdf(directory):
    all_species_records = []

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            try:
                text = extract_text_without_references(pdf_path)
                if len(text) < 100:
                    continue
                sentences = sent_tokenize(text)
                species_counter = Counter()

                for sentence in sentences:
                    doc = nlp(sentence)
                    for ent in doc.ents:
                        name = ent.text.strip()
                        if is_valid_species_gbif(name):
                            species_counter[name] += 1

                for species, freq in species_counter.items():
                    all_species_records.append({
                        "filename": filename,
                        "species": species,
                        "frequency": freq
                    })

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if all_species_records:
        df = pd.DataFrame(all_species_records)
        df = df.sort_values(by=["filename", "frequency"], ascending=[True, False])
        output_path = os.path.join(directory, "species_entities.csv")
        df.to_csv(output_path, index=False)
        print(f"✅ Species extraction saved to {output_path}")
    else:
        print("🚫 No species entities found. Skipping CSV save.")