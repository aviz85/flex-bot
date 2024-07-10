from base_chatbot import BaseChatBot

class EchoChatBot(BaseChatBot):
    def __init__(self, chatbot_id):
        super().__init__(chatbot_id)
        self.echo_prefix = self.settings.get('echo_prefix', 'Echo')

    def generate_response(self, input_text: str, thread: Thread) -> str:
        return f"{self.echo_prefix}: {input_text}"
