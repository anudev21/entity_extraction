import os
# entity_extraction_tool/main.py

import argparse
from extractors.country_extractor import extract_countries_from_pdf
from extractors.species_extractor import extract_species_from_pdf

def main():
    parser = argparse.ArgumentParser(description="Extract entities from PDFs.")
    parser.add_argument(
        "--directory",
        required=True,
        help="Path to directory containing PDFs"
    )
    parser.add_argument(
        "--entities",
        nargs="+",
        choices=["species", "country"],
        required=True,
        help="Entities to extract (choose one or more: species, country)"
    )
    args = parser.parse_args()

    for entity in args.entities:
        if entity == "country":
            extract_countries_from_pdf(args.directory)
        elif entity == "species":
            extract_species_from_pdf(args.directory)

if __name__ == "__main__":
    main()