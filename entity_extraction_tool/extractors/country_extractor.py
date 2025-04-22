import os
import spacy
import nltk
import re
import fitz  # PyMuPDF
from collections import Counter, defaultdict
import pandas as pd
from babel import Locale
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

nlp = spacy.load("en_core_web_lg")
ALL_COUNTRIES = set(Locale('en').territories.values())

def extract_text_without_references(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    # Strip reference section
    for pattern in [r'\nReferences\n.*', r'\nREFERENCES\n.*', r'\nBibliography\n.*']:
        text = re.split(pattern, text, flags=re.DOTALL)[0]
    return text.strip()

def extract_countries_from_pdf(directory):
    per_pdf_counts = defaultdict(Counter)
    global_counts = Counter()

    for filename in os.listdir(directory):
        if not filename.endswith(".pdf"):
            continue
        pdf_path = os.path.join(directory, filename)
        try:
            text = extract_text_without_references(pdf_path)
            if len(text) < 100:
                continue
            sentences = sent_tokenize(text)
            local_counts = Counter()
            for sentence in sentences:
                doc = nlp(sentence)
                for ent in doc.ents:
                    if ent.label_ == "GPE":
                        country = ent.text.strip()
                        if country in ALL_COUNTRIES:
                            local_counts[country] += 1
                            global_counts[country] += 1
            per_pdf_counts[filename] = local_counts
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    if not global_counts:
        print("🚫 No country entities found. Skipping CSV save.")
        return

    # Save to CSV
    df = pd.DataFrame(global_counts.items(), columns=["country", "frequency"])
    for filename, counts in per_pdf_counts.items():
        df[filename] = df["country"].map(lambda x: counts.get(x, 0))
    df = df.sort_values(by="frequency", ascending=False).reset_index(drop=True)
    output_path = os.path.join(directory, "country_entities.csv")
    df.to_csv(output_path, index=False)
    print(f"✅ Country extraction saved to {output_path}")