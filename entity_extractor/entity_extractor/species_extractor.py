import re
import spacy
import requests
from nltk import sent_tokenize
from collections import Counter, defaultdict

class SpeciesExtractor:
    def __init__(self):
        self.global_counts = Counter()
        self.per_pdf_counts = defaultdict(Counter)
        self.nlp = spacy.load("en_core_sci_md")

    def is_species_format(self, name):
        return bool(re.match(r"^[A-Z][a-z]+ [a-z]+$", name))

    def is_valid_species_gbif(self, name):
        try:
            r = requests.get("https://api.gbif.org/v1/species/match", params={"name": name}, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return data.get("matchType") == "EXACT" and data.get("rank") == "SPECIES"
            return False
        except Exception:
            return False

    def extract_from_text(self, text, pmcid):
        local_counter = Counter()
        sentences = sent_tokenize(text)
        for sentence in sentences:
            doc = self.nlp(sentence)
            for ent in doc.ents:
                name = ent.text.strip()
                if self.is_species_format(name) and self.is_valid_species_gbif(name):
                    local_counter[name] += 1
                    self.global_counts[name] += 1
        self.per_pdf_counts[pmcid] = local_counter

    def to_dataframe(self):
        import pandas as pd
        df = pd.DataFrame(self.global_counts.items(), columns=["Species", "Frequency"])
        for pmcid, counts in self.per_pdf_counts.items():
            df[pmcid] = df["Species"].map(lambda x: counts.get(x, 0))
        df = df.sort_values(by="Frequency", ascending=False).reset_index(drop=True)
        df.index += 1
        return df