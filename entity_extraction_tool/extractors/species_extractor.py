from entity_extraction_tool.utils.pdf_utils import extract_text_without_references
import spacy
import requests
from collections import Counter
import pandas as pd

# Load SciSpaCy model for species extraction
nlp = spacy.load("en_core_sci_md")

# GBIF species validation
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

def extract_species_from_pdf(pdf_path):
    text = extract_text_without_references(pdf_path)
    sentences = text.split('\n')  # Or use sentence tokenization if needed

    species_counter = Counter()

    for sentence in sentences:
        doc = nlp(sentence)
        for ent in doc.ents:
            name = ent.text.strip()
            if is_valid_species_gbif(name):  # GBIF check added
                species_counter[name] += 1

    # Prepare DataFrame with all species
    df = pd.DataFrame(species_counter.items(), columns=["Species", "Frequency"])
    df = df.sort_values(by='Frequency', ascending=False)
    
    # Save the result as CSV
    df.to_csv(f"{pdf_path}_species_frequencies.csv", index=False)
    print(f"Species frequencies saved to {pdf_path}_species_frequencies.csv")