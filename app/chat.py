import logging
import os

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

from app.templates.condense_prompt import CONDENSE_PROMPT
from app.templates.qa_prompt import QA_PROMPT
from app.tools.factory import get_database, get_embeddings

db = get_database()
embeddings = get_embeddings()

# logging.basicConfig(level=logging.DEBUG)


def ask():
    # pdf_qa = RetrievalQAWithSourcesChain.from_chain_type(
    #     llm=ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_GPT_MODEL")),
    #     retriever=db.as_retriever(),
    #     chain_type="refine",
    #     return_source_documents=True,
    # )
    # result = pdf_qa({"question": query})
    model = ChatOpenAI(
        model_name=os.getenv("OPENAI_GPT_MODEL"), temperature=0, streaming=True
    )
    retriever = db.as_retriever(
        search_kwargs={"k": 5},
        qa_template=QA_PROMPT,
        question_generator_template=CONDENSE_PROMPT,
    )
    qa = ConversationalRetrievalChain.from_llm(
        llm=model, retriever=retriever, return_source_documents=True
    )
    return qa


if __name__ == "__main__":
    while True:
        ask()
