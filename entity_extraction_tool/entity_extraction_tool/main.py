import argparse
import os
from extractors.country_extractor import extract_countries_from_pdf
from extractors.species_extractor import extract_species_from_pdf
# Add other extractors here as you implement them
# from extractors.disease_extractor import extract_diseases_from_pdf
# from extractors.method_extractor import extract_methods_from_pdf

def main():
    parser = argparse.ArgumentParser(description="Entity extractor for biodiversity PDFs")
    parser.add_argument("directory", type=str, help="Path to the directory containing PDFs")
    parser.add_argument("--entities", type=str, nargs="+", default=["country", "species"],
                        help="Entities to extract: country, species")

    args = parser.parse_args()
    directory = args.directory
    entities = args.entities

    if not os.path.isdir(directory):
        print(f"❌ Error: {directory} is not a valid directory.")
        return

    if "country" in entities:
        print("\n🌍 Extracting country entities...")
        extract_countries_from_pdf(directory)

    if "species" in entities:
        print("\n🌿 Extracting species entities...")
        extract_species_from_pdf(directory)

    # Future extensibility
    # if "disease" in entities:
    #     print("\n🦠 Extracting disease entities...")
    #     extract_diseases_from_pdf(directory)

    # if "method" in entities:
    #     print("\n⚗️ Extracting method entities...")
    #     extract_methods_from_pdf(directory)

if __name__ == "__main__":
    main()