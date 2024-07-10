# File: models/base_chatbot.py

import logging
from .message import Message
from .thread import Thread
from .content_item import ContentItem
from .text_content import TextContent
from flask import current_app

logger = logging.getLogger(__name__)

class BaseChatBot:
    def __init__(self, chatbot_id: str):
        self.chatbot = current_app.storage.get_chatbot(chatbot_id)
        if not self.chatbot:
            raise ValueError(f"Invalid chatbot ID: {chatbot_id}")
        self.settings = self.chatbot.settings

    def get_chat_response(self, message: Message, thread: Thread) -> Message:
        logger.debug(f"Processing message in ChatBot: {message}")
        
        response_content = self.generate_response(message, thread)

        
        assistant_message = current_app.storage.create_message(
            thread_id=thread.id,
            role="assistant",
            content=response_content,
            metadata={"chatbot_id": self.chatbot.id}
        )
        
        logger.debug(f"Generated response: {assistant_message}")
        return assistant_message

    def generate_response(self, message: Message, thread: Thread) -> str:
        raise NotImplementedError("Subclasses must implement generate_response method")

class BaseTextChatBot(BaseChatBot):
    def generate_response(self, message: Message, thread: Thread) -> str:
        input_text = message.content[0].text.value if message.content else ""
        return self.process_text(input_text)

    def process_text(self, input_text: str) -> str:
        raise NotImplementedError("Subclasses must implement process_text method")

class BaseConversationalChatBot(BaseChatBot):
    def generate_response(self, message: Message, thread: Thread) -> str:
        input_text = message.content[0].text.value if message.content else ""
        conversation_history = self.get_conversation_history(thread)
        return self.process_conversation(input_text, conversation_history)

    def get_conversation_history(self, thread: Thread, max_messages: int = 10) -> list:
        history = []
        for msg in thread.messages[-max_messages:]:
            print(f'IM HERE PRINTING MESSAGE: {msg}')
            role = "assistant" if msg['role'] == "assistant" else "user"
            print(f'!!!!IM HERE!!!!!')
            content = msg.get('content', [{}])[0].get('text', {}).get('value', "")
            history.append({"role": role, "content": content})
        return history

    def process_conversation(self, input_text: str, conversation_history: list) -> str:
        raise NotImplementedError("Subclasses must implement process_conversation method")