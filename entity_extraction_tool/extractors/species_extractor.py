import os
import re
import fitz  # PyMuPDF
import spacy
import nltk
import requests
import pandas as pd
from nltk.tokenize import sent_tokenize
from collections import Counter, defaultdict

nltk.download("punkt")

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

def extract_text_without_references(pdf_path):
    full_text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            full_text += page.get_text()
    patterns = [r'\nReferences\n.*', r'\nREFERENCES\n.*', r'\nBibliography\n.*']
    for pattern in patterns:
        full_text = re.split(pattern, full_text, flags=re.DOTALL)[0]
    return full_text.strip()

def is_species_format(text):
    return bool(re.match(r"^[A-Z][a-z]+ [a-z]+$", text.strip()))

def extract_species_from_pdf(directory):
    global_species_counter = Counter()
    per_pdf_species_counter = defaultdict(Counter)

    for filename in os.listdir(directory):
        if not filename.endswith(".pdf"):
            continue
        pdf_path = os.path.join(directory, filename)
        try:
            text = extract_text_without_references(pdf_path)
            if len(text) < 100:
                continue
            sentences = sent_tokenize(text)
            local_species_counter = Counter()
            for sentence in sentences:
                doc = nlp(sentence)
                for ent in doc.ents:
                    name = ent.text.strip()
                    if is_species_format(name) and is_valid_species_gbif(name):
                        local_species_counter[name] += 1
                        global_species_counter[name] += 1
            per_pdf_species_counter[filename] = local_species_counter
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    if not global_species_counter:
        print("🚫 No species entities found. Skipping CSV save.")
        return

    df = pd.DataFrame(global_species_counter.items(), columns=["Species", "Frequency"])
    for filename, counter in per_pdf_species_counter.items():
        df[filename] = df["Species"].map(lambda x: counter.get(x, 0))
    df = df.sort_values(by="Frequency", ascending=False).reset_index(drop=True)
    output_path = os.path.join(directory, "species_entities.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Species extraction saved to {output_path}")
