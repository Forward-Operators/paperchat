import json
import os

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from templates.condense_prompt import CONDENSE_PROMPT
from templates.qa_prompt import QA_PROMPT
from tools.factory import get_database

db = get_database()


def chat(query):
    chat_history = []
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
    result = qa({"question": query, "chat_history": chat_history})
    answer = {}
    answer["answer"] = result["answer"]
    source_documents = result["source_documents"]
    parsed_documents = []
    for doc in source_documents:
        parsed_doc = {
                "metadata": {
                    "page_number": doc.metadata.get("page_number", 0),
                    "source": doc.metadata.get("source", ""),
                },
            }
        parsed_documents.append(parsed_doc)
    answer["sources"] = parsed_documents
    json_data = json.dumps(answer)
    return json_data
