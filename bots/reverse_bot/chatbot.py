# File: bots/reverse_bot/chatbot.py

from models import BaseTextChatBot

class ChatBot(BaseTextChatBot):
    def __init__(self, chatbot_id):
        super().__init__(chatbot_id)

    def process_text(self, input_text: str) -> str:
        return f"Reversed: {input_text[::-1]}"