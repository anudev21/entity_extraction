import fitz
import re

def extract_text_without_references(pdf_path):
    full_text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            full_text += page.get_text()
    patterns = [
        r'\nReferences\n.*',
        r'\nREFERENCES\n.*',
        r'\nBibliography\n.*',
    ]
    for pattern in patterns:
        full_text = re.split(pattern, full_text, flags=re.DOTALL)[0]
    return full_text.strip()