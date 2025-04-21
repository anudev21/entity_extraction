from setuptools import setup, find_packages

setup(
    name='entity_extraction_tool',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'spacy',
        'scispacy',
        'nltk',
        'pymupdf',
        'requests',
        'pandas',
        'babel',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'extract-entities=entity_extraction_tool.main:main',
        ],
    },
    include_package_data=True,
    author='Your Name',
    description='CLI tool to extract species and countries from PDFs downloaded using pygetpapers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/entity_extraction_tool',  # Update if pushing to GitHub
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)