import os

from chromadb.config import Settings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma


def chat():
    embeddings = OpenAIEmbeddings()
    chroma_settings = Settings(
        chroma_api_impl="rest",
        chroma_server_host=os.environ(CHROMA_HOST, "localhost"),
        chroma_server_http_port=os.environ(CHROMA_PORT, "8000"),
    )
    vectordb = Chroma(embedding_function=embeddings, client_settings=chroma_settings)
    pdf_qa = ConversationalRetrievalChain.from_llm(
        OpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
        vectordb.as_retriever(),
        return_source_documents=True,
    )
    chat_history = []
    print("What would you like to ask?")
    query = input()
    result = pdf_qa({"question": query, "chat_history": chat_history})
    print("Answer:")
    print(result["answer"])
    print("Source:")
    print(result["source_documents"])


if __name__ == "__main__":
    while True:
        chat()
