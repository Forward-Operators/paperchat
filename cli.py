import json

from dotenv import load_dotenv
import logging
from app.chat import ask
logging.basicConfig(level=logging.DEBUG)
load_dotenv()


def chat_loop():
    chat_history = []
    while True:
        query = input("Please enter your question (or type 'exit' to end): ")
        if query.lower() == "exit":
            break
        process = ask()
        result = process({"question": query, "chat_history": chat_history})

        print(result["answer"])
        source_documents = result["source_documents"]
        parsed_documents = []
        for doc in source_documents:
            parsed_doc = {
                "page_content": doc.page_content,
                "metadata": {
                    "author": doc.metadata.get("author", ""),
                    "creationDate": doc.metadata.get("creationDate", ""),
                    "creator": doc.metadata.get("creator", ""),
                    "file_path": doc.metadata.get("file_path", ""),
                    "format": doc.metadata.get("format", ""),
                    "keywords": doc.metadata.get("keywords", ""),
                    "modDate": doc.metadata.get("modDate", ""),
                    "page_number": doc.metadata.get("page_number", 0),
                    "producer": doc.metadata.get("producer", ""),
                    "source": doc.metadata.get("source", ""),
                    "subject": doc.metadata.get("subject", ""),
                    "title": doc.metadata.get("title", ""),
                    "total_pages": doc.metadata.get("total_pages", 0),
                    "trapped": doc.metadata.get("trapped", ""),
                },
            }
            parsed_documents.append(parsed_doc)
        for doc in parsed_documents:
            print(doc["metadata"]["source"])
            print(doc["metadata"]["page_number"])

        chat_history.append((query, result["answer"]))
        with open("chat_history.json", "w") as json_file:
            json.dump(chat_history, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    chat_loop()
