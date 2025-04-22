import os
import spacy
import pandas as pd
from collections import Counter, defaultdict
from utils.pdf_utils import extract_text_without_references
from nltk.tokenize import sent_tokenize
from babel import Locale

nlp = spacy.load("en_core_web_lg")

all_countries_list = set(Locale('en').territories.values())

def is_country(text):
    return text.strip() in all_countries_list

def extract_countries_from_pdf(directory):
    all_country_records = []

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            try:
                text = extract_text_without_references(pdf_path)
                if len(text) < 100:
                    continue
                sentences = sent_tokenize(text)
                country_counter = Counter()

                for sentence in sentences:
                    doc = nlp(sentence)
                    for ent in doc.ents:
                        if ent.label_ == "GPE":
                            country = ent.text.strip()
                            if is_country(country):
                                country_counter[country] += 1

                for country, freq in country_counter.items():
                    all_country_records.append({
                        "filename": filename,
                        "country": country,
                        "frequency": freq
                    })

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if all_country_records:
        df = pd.DataFrame(all_country_records)
        df = df.sort_values(by=["filename", "frequency"], ascending=[True, False])
        output_path = os.path.join(directory, "country_entities.csv")
        df.to_csv(output_path, index=False)
        print(f"✅ Country extraction saved to {output_path}")
    else:
        print("🚫 No country entities found. Skipping CSV save.")