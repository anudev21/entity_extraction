from entity_extraction_tool.utils.pdf_utils import extract_text_without_references
import spacy
from collections import Counter
import pandas as pd

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

def extract_countries_from_pdf(pdf_path):
    text = extract_text_without_references(pdf_path)
    doc = nlp(text)
    
    countries = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
    country_counts = Counter(countries)
    
    df = pd.DataFrame(country_counts.items(), columns=["Country", "Frequency"])
    df = df.sort_values(by='Frequency', ascending=False)
    
    # Save the result as CSV
    df.to_csv(f"{pdf_path}_country_frequencies.csv", index=False)
    print(f"Country frequencies saved to {pdf_path}_country_frequencies.csv")