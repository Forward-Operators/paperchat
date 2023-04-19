import logging
import os

import arxiv
from chromadb.config import Settings
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

logging.basicConfig(level=logging.INFO)


def load_to_chroma(pdf_path):
    chroma_settings = Settings(
        chroma_api_impl="rest",
        chroma_server_host="localhost",
        chroma_server_http_port=8000,
        anonymized_telemetry=False,
    )

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    for filename in os.listdir(pdf_path):
        f = os.path.join(pdf_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            loader = PyPDFLoader(f)
            pages = loader.load_and_split()
            Chroma.from_documents(
                pages, embedding=embeddings, client_settings=chroma_settings
            )


def load_from_remote(pdf_url):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    chroma_settings = Settings(
        chroma_api_impl="rest",
        chroma_server_host="localhost",
        chroma_server_http_port=8000,
        anonymized_telemetry=False,
    )

    print(f"Loading {pdf_url}")
    logging.info(f"Loading {pdf_url}")
    loader = PyPDFLoader(pdf_url)
    pages = loader.load_and_split()
    Chroma.from_documents(
        collection_name="arxiv",
        documents=pages,
        embedding=embeddings,
        client_settings=chroma_settings,
    )


def load_data():
    """Load data from arxiv"""
    docs_path = "./docs"
    print("What would you like to search for?")
    category = input()
    papers = arxiv.Search(
        query=f'ti:"{category}"',
        max_results=15,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    for paper in papers.results():
        # paper.download_pdf(dirpath=docs_path)
        load_from_remote(paper.pdf_url)
    # load_to_chroma(docs_path)


if __name__ == "__main__":
    load_data()
