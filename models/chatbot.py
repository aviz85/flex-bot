from dataclasses import dataclass, field
from typing import Dict
from datetime import datetime

@dataclass
class Chatbot:
    id: str
    chatbot_type_id: str
    name: str
    created_at: int = field(default_factory=lambda: int(datetime.now().timestamp()))
    settings: Dict = field(default_factory=dict)
   
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "chatbot_type_id": self.chatbot_type_id,
            "name": self.name,
            "created_at": self.created_at,
            "settings": self.settings
        }