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
        thread.add_message(message)
        
        # Generate response (implementation depends on the specific bot)
        response_content = f"Default response: {message.content[0].text.value}"
        
        assistant_message = Message(
            role="assistant",
            content=[ContentItem(text=TextContent(response_content))]
        )
        thread.add_message(assistant_message)
        
        logger.debug(f"Generated response: {assistant_message}")
        return assistant_message