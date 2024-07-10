# File: bots/claude/chatbot.py

from models import BaseConversationalChatBot
from .anthropic_api_client import AnthropicAPIClient
from .message_utils import filter_messages

class ChatBot(BaseConversationalChatBot):
    def __init__(self, chatbot_id):
        super().__init__(chatbot_id)
        self.anthropic_client = AnthropicAPIClient()
        self.system_prompt = """You are a sarcastic friend chatbot. Your responses should be witty, 
        slightly edgy, and filled with playful sarcasm. However, always remain friendly and avoid being 
        overly mean or offensive. Your goal is to entertain and engage in lighthearted banter."""

    def process_conversation(self, input_text: str, conversation_history: list) -> str:
        # Prepare the messages for the Anthropic API
        messages = conversation_history + [{"role": "user", "content": input_text}]
        filtered_messages = filter_messages(messages)
        
        try:
            # Call the Anthropic API
            api_response = self.anthropic_client.call_anthropic_api(filtered_messages, self.system_prompt)
            
            # Extract the response text from the API response
            response_text = api_response['content'][0]['text']
        except ValueError as e:
            response_text = f"Error: {str(e)}. Please try starting a new conversation."
        except Exception as e:
            response_text = f"An error occurred: {str(e)}. Please try again later."
        
        return response_text