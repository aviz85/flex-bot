# File: bots/claude/anthropic_api_client.py

import os
import requests

class AnthropicAPIClient:
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")

    def call_anthropic_api(self, messages, system_prompt):
        headers = {
            "content-type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": 150,
            "messages": messages,
            "system": system_prompt
        }
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        return response.json()