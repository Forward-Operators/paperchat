import logging
import os

from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PDFMinerLoader
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.tools.factory import get_embeddings, get_database

# logging.basicConfig(level=logging.DEBUG)

embeddings = get_embeddings()
db = get_database()


def load_data():
    docs_path = "/mnt/datasets/arxiv/pdf/"
    for filename in os.listdir(docs_path):
        f = os.path.join(docs_path, filename)
        if os.path.isfile(f):
            try:
                loader = PDFMinerLoader(f)
                print(f"Loading {f}")
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, chunk_overlap=300, length_function=len,
                )
                documents = loader.load_and_split(text_splitter=text_splitter)
                db.add_documents(documents)
            except Exception:
                continue


def questions(query):
    chain = RetrievalQAWithSourcesChain.from_chain_type(ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_GPT_MODEL")), chain_type="refine", retriever=db.as_retriever())
    result = chain({"question": query})
    return result


if __name__ == "__main__":
    load_data()
