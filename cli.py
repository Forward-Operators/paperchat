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
        result = ask(query)

        print(result)


if __name__ == "__main__":
    chat_loop()
