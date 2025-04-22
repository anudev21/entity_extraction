import spacy
from nltk import sent_tokenize
from babel import Locale
from collections import Counter, defaultdict

class CountryExtractor:
    def __init__(self):
        self.global_counts = Counter()
        self.per_pdf_counts = defaultdict(Counter)
        self.all_countries_list = set(Locale('en').territories.values())
        self.nlp = spacy.load("en_core_web_lg")

    def is_country(self, text):
        return text.strip() in self.all_countries_list

    def extract_from_text(self, text, pmcid):
        local_counter = Counter()
        sentences = sent_tokenize(text)
        for sentence in sentences:
            doc = self.nlp(sentence)
            for ent in doc.ents:
                if ent.label_ == "GPE" and self.is_country(ent.text.strip()):
                    country = ent.text.strip()
                    local_counter[country] += 1
                    self.global_counts[country] += 1
        self.per_pdf_counts[pmcid] = local_counter

    def to_dataframe(self):
        import pandas as pd
        df = pd.DataFrame(self.global_counts.items(), columns=["Country", "Frequency"])
        for pmcid, counts in self.per_pdf_counts.items():
            df[pmcid] = df["Country"].map(lambda x: counts.get(x, 0))
        df = df.sort_values(by="Frequency", ascending=False).reset_index(drop=True)
        df.index += 1
        return df