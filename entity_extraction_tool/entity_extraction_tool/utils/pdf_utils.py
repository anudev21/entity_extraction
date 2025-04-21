import fitz  # PyMuPDF
import re

def extract_text_without_references(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    
    # Remove references section if present
    patterns = [r'\nReferences\n.*', r'\nREFERENCES\n.*', r'\nBibliography\n.*']
    for pattern in patterns:
        text = re.split(pattern, text, flags=re.DOTALL)[0]
    
    return text.strip()