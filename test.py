import logging
import os

from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.tools.factory import get_embeddings, get_database

logging.basicConfig(level=logging.DEBUG)

embeddings = get_embeddings()
db = get_database()


def load_data():
    docs_path = "/mnt/tmp/datasets/arxiv/test2/"
    for filename in os.listdir(docs_path):
        f = os.path.join(docs_path, filename)
        if os.path.isfile(f):
            try:
                loader = PyPDFLoader(f)
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=2000, chunk_overlap=100
                )
                documents = loader.load_and_split(text_splitter=text_splitter)
                db.add_documents(documents)
            except Exception:
                continue


def questions():
    llm = ChatOpenAI(temperature=0, model_name=os.environ.get("OPENAI_GPT_MODEL"))
    chain = load_qa_chain(llm, chain_type="stuff")
    query = input("Question:")
    docs = db.similarity_search(query=query, k=2)
    result = chain.run(input_documents=docs, question=query)
    print(result)


if __name__ == "__main__":
    load_data()
    # questions()
