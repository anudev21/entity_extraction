from setuptools import setup, find_packages

setup(
    name="entity_extraction_tool",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'spacy', 'requests', 'beautifulsoup4', 'lxml', 'nltk', 'tqdm', 'pyMuPDF', 'scispacy', 'pandas', 'babel',
    ],
    entry_points={
        'console_scripts': [
            'extract-entities = entity_extraction_tool.main:main',  # This links the CLI to the main function
        ],
    },
)