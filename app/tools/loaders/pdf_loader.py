import logging
import os

import arxiv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tools.factory import get_database, get_embeddings

logging.basicConfig(level=logging.INFO)

embeddings = get_embeddings()
db = get_database()


def load_to_database(pdf_path):
    for filename in os.listdir(pdf_path):
        f = os.path.join(pdf_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=300,
                length_function=len,
            )
            loader = PyPDFLoader(f)
            pages = loader.load_and_split(text_splitter=text_splitter)
            db.add_documents(documents=pages)


def load_from_remote(pdf_url):
    print(f"Loading {pdf_url}")
    logging.info(f"Loading {pdf_url}")
    loader = PyPDFLoader(pdf_url)
    pages = loader.load_and_split()
    db.add_documents(documents=pages)


def load_data():
    """
    Loads data from arxiv for given category
    Limited to 150 results, but you can change it
    """
    docs_path = "/mnt/datasets/arxiv/pdf/"
    print("What would you like to search for?")
    category = input()
    papers = arxiv.Search(
        query=f'ti:"{category}"',
        max_results=150,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    for paper in papers.results():
        paper.download_pdf(dirpath=docs_path)
        # load_from_remote(paper.pdf_url) <- you can use this if you want to load from remote url directly
        load_to_database(docs_path)


if __name__ == "__main__":
    load_data()
