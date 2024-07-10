from base_chatbot import BaseChatBot

class AnthropicChatBot(BaseChatBot):
    def __init__(self, chatbot_id):
        super().__init__(chatbot_id)
        self.system_prompt = self.settings.get('system_prompt', "You are a helpful assistant.")
        self.model = self.settings.get('model', "claude-3-5-sonnet-20240620")
        self.max_tokens = self.settings.get('max_tokens', 150)

    def generate_response(self, input_text: str, thread: Thread) -> str:
        messages = self._prepare_messages(input_text, thread)
        api_response = self._call_api(messages)
        return api_response['content'][0]['text']

    def _prepare_messages(self, input_text, thread):
        messages = [{"role": "user", "content": input_text}]
        for prev_message in thread.messages[-5:]:
            role = "assistant" if prev_message.role == "assistant" else "user"
            content = prev_message.content[0].text.value if prev_message.content else ""
            messages.insert(-1, {"role": role, "content": content})
        return messages

    def _call_api(self, messages):
        return self.anthropic_client.call_anthropic_api({
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages,
            "system": self.system_prompt
        })