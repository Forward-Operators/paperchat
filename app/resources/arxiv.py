import json

from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from tools.factory import get_embeddings, get_database

embeddings = get_embeddings()
db = get_database()


def chat(query):
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = db.similarity_search(query=query, k=5)
    # chat_history = []
    result = chain.run(input_documents=docs, question=query)
    answer = {}
    answer["answer"] = result["answer"]
    answer["source"] = result["source_documents"][0].metadata
    json_data = json.dumps(answer)
    return json_data
