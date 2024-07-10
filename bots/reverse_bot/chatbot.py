from models import BaseChatBot, Message, Thread, ContentItem, TextContent

class ChatBot(BaseChatBot):
    def __init__(self, chatbot_id):
        super().__init__(chatbot_id)
        self.echo_prefix = self.settings.get('echo_prefix', 'Echo')

    def get_chat_response(self, message: Message, thread: Thread) -> Message:
        # Extract the text content from the input message
        input_text = message.content[0].text.value if message.content else ""
        
        # Reverse the user's message
        original_content = message.content[0].text.value
        response_text = f"Reversed: {original_content[::-1]}"
        
        # Create a new message with the response
        response_message = Message(
            role="assistant",
            content=[ContentItem(text=TextContent(response_text))],
            thread_id=thread.id,
            chatbot_id=self.chatbot.id
        )
        
        # Add the response message to the thread
        thread.add_message(response_message)
        
        return response_message
