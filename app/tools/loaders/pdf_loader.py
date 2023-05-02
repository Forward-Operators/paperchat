import logging
import os
from tools.factory import get_embeddings, get_database

import arxiv
from langchain.document_loaders import PyPDFLoader

logging.basicConfig(level=logging.INFO)

embeddings = get_embeddings()
db = get_database()


def load_to_database(pdf_path):
    for filename in os.listdir(pdf_path):
        f = os.path.join(pdf_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            loader = PyPDFLoader(f)
            pages = loader.load_and_split()
            db.add_documents(documents=pages)


def load_from_remote(pdf_url):
    print(f"Loading {pdf_url}")
    logging.info(f"Loading {pdf_url}")
    loader = PyPDFLoader(pdf_url)
    pages = loader.load_and_split()
    db.add_documents(documents=pages)


def load_data():
    """Load data from arxiv"""
    docs_path = "./docs"
    print("What would you like to search for?")
    category = input()
    papers = arxiv.Search(
        query=f'ti:"{category}"',
        max_results=150,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    for paper in papers.results():
        paper.download_pdf(dirpath=docs_path)
        load_from_remote(paper.pdf_url)
        load_to_database(docs_path)


if __name__ == "__main__":
    load_data()
