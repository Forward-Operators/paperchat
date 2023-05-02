import logging

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from app.tools.factory import get_database

db = get_database()

logging.basicConfig(level=logging.DEBUG)


def ask(query):
    # pdf_qa = RetrievalQAWithSourcesChain.from_chain_type(
    #     llm=ChatOpenAI(temperature=0, model_name=os.getenv("OPENAI_GPT_MODEL")),
    #     retriever=db.as_retriever(),
    #     chain_type="map_reduce",
    #     return_source_documents=True,
    # )
    # llm = ChatOpenAI(temperature=0, model_name=os.environ.get("OPENAI_GPT_MODEL"))
    # chain = load_qa_chain(llm, chain_type="stuff")
    docs = db.similarity_search(query=query, k=5)
    print(docs)
    result = docs
    # result = chain.run(input_documents=docs, question=query)
    # chat_history = []
    # result = pdf_qa({"question": query, "chat_history": chat_history})
    return result


if __name__ == "__main__":
    while True:
        ask()
