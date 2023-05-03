import logging
import os

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from app.tools.factory import get_database, get_embeddings

db = get_database()
embeddings = get_embeddings()

# logging.basicConfig(level=logging.DEBUG)


def ask(query):
    pdf_qa = RetrievalQAWithSourcesChain.from_chain_type(
        llm=ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_GPT_MODEL")),
        retriever=db.as_retriever(),
        chain_type="refine",
        return_source_documents=True,
    )
    result = pdf_qa({"question": query})
    return result


if __name__ == "__main__":
    while True:
        ask()
