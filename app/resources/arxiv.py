import json
import os

from chromadb.config import Settings
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma


def chat(query):
    embeddings = OpenAIEmbeddings()
    chroma_settings = Settings(
        chroma_api_impl="rest",
        chroma_server_host=os.getenv("CHROMA_HOST", "localhost"),
        chroma_server_http_port=os.getenv("CHROMA_PORT", "8000"),
    )
    vectordb = Chroma(embedding_function=embeddings, client_settings=chroma_settings)
    pdf_qa = ConversationalRetrievalChain.from_llm(
        OpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
        vectordb.as_retriever(),
        return_source_documents=True,
    )
    chat_history = []
    result = pdf_qa({"question": query, "chat_history": chat_history})
    answer = {}
    answer["answer"] = result["answer"]
    answer["source"] = result["source_documents"][0].metadata
    json_data = json.dumps(answer)
    return json_data
