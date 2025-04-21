import fitz  # PyMuPDF
import re
from babel import Locale
from nltk.tokenize import sent_tokenize
import requests

# Load all official country names from Babel
all_countries = set(Locale('en').territories.values())


def extract_text_without_references(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    # Remove References/Bibliography section if found
    patterns = [r'\nReferences\n.*', r'\nREFERENCES\n.*', r'\nBibliography\n.*']
    for pattern in patterns:
        text = re.split(pattern, text, flags=re.DOTALL)[0]
    return text.strip()


def is_country(text):
    return text.strip() in all_countries


def is_species_format(text):
    """
    Check if the text looks like a Latin binomial name.
    Example: 'Homo sapiens'
    """
    return bool(re.match(r"^[A-Z][a-z]+ [a-z]+$", text.strip()))


def is_valid_species_gbif(name):
    """
    Validate species name using GBIF API.
    """
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


def split_sentences(text):
    return sent_tokenize(text)