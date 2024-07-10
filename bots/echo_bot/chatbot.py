# File: bots/echo_bot/chatbot.py

from models import BaseTextChatBot

class ChatBot(BaseTextChatBot):
    def __init__(self, chatbot_id):
        super().__init__(chatbot_id)
        self.echo_prefix = self.settings.get('echo_prefix', 'Echo')

    def process_text(self, input_text: str) -> str:
        return f"{self.echo_prefix}: {input_text}"