import logging

import arxiv
from chromadb.config import Settings
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


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


def load_data(category):
    """Load data from arxiv"""
    papers = arxiv.Search(
        query=f'ti:"{category}"',
        max_results=150,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    for paper in papers.results():
        load_from_remote(paper.pdf_url)
