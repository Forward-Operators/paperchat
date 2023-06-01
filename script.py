import logging
import os

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyMuPDFLoader, PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.tools.factory import get_database, get_embeddings

# logging.basicConfig(level=logging.DEBUG)

embeddings = get_embeddings()
db = get_database()


def load_data():
    docs_path = "/mnt/dataset/arxiv/pdf"
    for filename in os.listdir(docs_path):
        f = os.path.join(docs_path, filename)
        if os.path.isfile(f):
            try:
                loader = PDFPlumberLoader(f)
                print(f"Loading {f}")
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=2000,
                    chunk_overlap=100,
                    length_function=len,
                )
                documents = loader.load_and_split(text_splitter=text_splitter)
                # print(documents)
                db.add_documents(documents)
            except Exception as e:
                print(e)
                continue


def questions(query):
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_GPT_MODEL")),
        chain_type="stuff",
        retriever=db.as_retriever(),
    )
    result = chain({"question": query})
    return result


if __name__ == "__main__":
    load_data()
