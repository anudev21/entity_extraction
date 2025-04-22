import os
from wildlife_extractor.text_utils import extract_text_without_references
from wildlife_extractor.country_extractor import CountryExtractor
from wildlife_extractor.species_extractor import SpeciesExtractor
from tqdm import tqdm

def get_pdf_files(folder_path):
    pdf_files = []
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower() == "fulltext.pdf":
                pdf_files.append(os.path.join(dirpath, filename))
    return pdf_files

def main(folder_path):
    pdf_files = get_pdf_files(folder_path)
    print(f"✅ Found {len(pdf_files)} PDFs")

    country_extractor = CountryExtractor()
    species_extractor = SpeciesExtractor()

    for pdf in tqdm(pdf_files, desc="Processing PDFs"):
        text = extract_text_without_references(pdf)
        if len(text) < 100:
            continue
        pmcid = os.path.basename(os.path.dirname(pdf))
        country_extractor.extract_from_text(text, pmcid)
        species_extractor.extract_from_text(text, pmcid)

    # Save results
    country_df = country_extractor.to_dataframe()
    if not country_df.empty:
        country_df.to_csv("country_frequency_with_pmc.csv", index=False)
        print("🌍 Country CSV saved.")
    else:
        print("🚫 No country entities found.")

    species_df = species_extractor.to_dataframe()
    if not species_df.empty:
        species_df.to_csv("species_frequency_with_pmc.csv", index=False)
        print("🌿 Species CSV saved.")
    else:
        print("🚫 No species entities found.")
