import os
import spacy
from collections import Counter
import pandas as pd
from utils.pdf_utils import extract_text_without_references

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print("Model 'en_core_web_lg' not found. Please install it using: pip install en_core_web_lg")

def extract_countries_from_pdf(directory):
    all_country_records = []

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            try:
                text = extract_text_without_references(pdf_path)
                doc = nlp(text)
                countries = [ent.text.strip() for ent in doc.ents if ent.label_ == "GPE"]
                country_counts = Counter(countries)

                for country, freq in country_counts.items():
                    all_country_records.append({
                        "filename": filename,
                        "country": country,
                        "frequency": freq
                    })

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Save all to one CSV
    output_path = os.path.join(directory, "country_entities.csv")
    if all_country_records:
        df = pd.DataFrame(all_country_records)
        df = df.sort_values(by=["filename", "frequency"], ascending=[True, False])
        df.to_csv(output_path, index=False)
        print(f"Country extraction saved to {output_path}")
    else:
        print("No country entities found. Skipping CSV save.")