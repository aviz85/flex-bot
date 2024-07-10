import os
import requests
from models import BaseChatBot, Message, Thread, ContentItem, TextContent

class AnthropicAPIClient:
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")

    def call_anthropic_api(self, data):
        headers = {
            "content-type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        return response.json()

class ChatBot(BaseChatBot):
    def __init__(self, chatbot_id):
        super().__init__(chatbot_id)
        self.anthropic_client = AnthropicAPIClient()
        self.system_prompt = """You are a sarcastic friend chatbot. Your responses should be witty, 
        slightly edgy, and filled with playful sarcasm. However, always remain friendly and avoid being 
        overly mean or offensive. Your goal is to entertain and engage in lighthearted banter."""

    def get_chat_response(self, message: Message, thread: Thread) -> Message:
        # Extract the text content from the input message
        input_text = message.content[0].text.value if message.content else ""
        
        # Prepare the messages for the Anthropic API
        messages = [
            {"role": "user", "content": input_text}
        ]
        
        # Add previous messages from the thread to provide context
        for prev_message in thread.messages[-5:]:  # Include up to 5 previous messages
            role = "assistant" if prev_message.role == "assistant" else "user"
            content = prev_message.content[0].text.value if prev_message.content else ""
            messages.insert(-1, {"role": role, "content": content})
        
        # Call the Anthropic API
        api_response = self.anthropic_client.call_anthropic_api({
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": 150,
            "messages": messages,
            "system": self.system_prompt
        })
        
        # Extract the response text from the API response
        response_text = api_response['content'][0]['text']
        
        # Create a new message with the response
        response_message = Message(
            role="assistant",
            content=[ContentItem(text=TextContent(response_text))],
            thread_id=thread.id,
            chatbot_id=self.chatbot.id
        )
        
        # Add the response message to the thread
        thread.add_message(response_message)
        
        # Return the response message
        return response_message