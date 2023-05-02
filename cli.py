import json
from app.chat import ask
from dotenv import load_dotenv

load_dotenv()


def chat_loop():
    chat_history = []
    while True:
        query = input("Please enter your question (or type 'exit' to end): ")
        if query.lower() == "exit":
            break
        # result = ask({"question": query, "chat_history": chat_history})
        result = ask(query)

        print(result["answer"])
        chat_history.append((query, result["answer"]))

        # Write chat history to a JSON file
        with open("chat_history.json", "w") as json_file:
            json.dump(chat_history, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    chat_loop()
