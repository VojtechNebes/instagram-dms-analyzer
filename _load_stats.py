import json
import os


def load_chat(chat_name: str):
    with open(os.path.join("statistics", chat_name, "message.json"), "rt") as chat_file:
        return json.load(chat_file)


def load_all_chats():
    return {chat_name: load_chat(chat_name) for chat_name in os.listdir("statistics")}