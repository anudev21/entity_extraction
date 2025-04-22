from setuptools import setup, find_packages

setup(
    name="wildlife_extractor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "spacy",
        "scispacy",
        "nltk",
        "tqdm",
        "PyMuPDF",
        "babel",
        "requests",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "wildlife-extractor=cli:run"
        ]
    },
)