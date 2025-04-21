import os
import argparse
from extractors.country_extractor import extract_countries_from_folder
from extractors.species_extractor import extract_species_from_folder

def main():
    parser = argparse.ArgumentParser(description="Extract species and countries from PDFs in a directory.")
    parser.add_argument("directory", help="Directory containing PDF files (e.g., disease_india)")
    parser.add_argument("--entities", choices=["species", "countries", "both"], default="both",
                        help="Which entities to extract (default: both)")

    args = parser.parse_args()
    pdf_folder = args.directory

    if not os.path.isdir(pdf_folder):
        print(f"Error: Directory '{pdf_folder}' does not exist.")
        return

    if args.entities in ("countries", "both"):
        extract_countries_from_folder(pdf_folder)

    if args.entities in ("species", "both"):
        extract_species_from_folder(pdf_folder)

if __name__ == "__main__":
    main()