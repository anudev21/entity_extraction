import argparse
from run_extraction import main

def run():
    parser = argparse.ArgumentParser(description="Extract country and species from PDF folder.")
    parser.add_argument("--folder", type=str, required=True, help="Path to the folder containing PDFs.")
    args = parser.parse_args()

    main(args.folder)

if __name__ == "__main__":
    run()