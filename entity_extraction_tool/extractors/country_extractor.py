import spacy
from babel import Locale
from collections import Counter
import pandas as pd
import os
from utils.pdf_utils import extract_text_without_references

nlp = spacy.load("en_core_web_lg")
all_countries = set(Locale('en').territories.values())

def is_country(text):
    return text.strip() in all_countries

def extract_countries_from_folder(folder_path):
    all_counts = Counter()
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_without_references(pdf_path)
            doc = nlp(text)
            countries = [ent.text for ent in doc.ents if ent.label_ == "GPE" and is_country(ent.text)]
            all_counts.update(countries)

    df = pd.DataFrame(all_counts.items(), columns=["Country", "Frequency"]).sort_values(by="Frequency", ascending=False)
    output_csv = os.path.join(folder_path, "countries_frequency.csv")
    df.to_csv(output_csv, index=False)
    print(f"[✓] Saved country frequencies to: {output_csv}")