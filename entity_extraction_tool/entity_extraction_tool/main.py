import os
import argparse
from extractors.country_extractor import extract_countries_from_pdf
from extractors.species_extractor import extract_species_from_pdf


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract entities (species, countries) from PDFs.")
    parser.add_argument('directory', type=str, help="Directory containing the PDFs to process")
    parser.add_argument('--entities', type=str, nargs='+', default=['species', 'country'], help="List of entities to extract (species, country)")
    
    # Parse the arguments
    args = parser.parse_args()

    # Iterate through files in the given directory
    for filename in os.listdir(args.directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(args.directory, filename)
            print(f"Processing: {pdf_path}")

            # Extract entities based on the user's choice
            if 'country' in args.entities:
                print("Extracting countries...")
                extract_countries_from_pdf(pdf_path)

            if 'species' in args.entities:
                print("Extracting species...")
                extract_species_from_pdf(pdf_path)

if __name__ == '__main__':
    main()