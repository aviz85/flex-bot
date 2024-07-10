from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import logging
from .message import Message

logger = logging.getLogger(__name__)

@dataclass
class Thread:
    id: str = field(default_factory=lambda: f"thread_{uuid.uuid4().hex[:6]}")
    created_at: int = field(default_factory=lambda: int(datetime.now().timestamp()))
    metadata: Dict = field(default_factory=dict)
    messages: List[Message] = field(default_factory=list)
    chatbot_id: Optional[str] = None

    def add_message(self, message: Message):
        message.thread_id = self.id
        self.messages.append(message)
        print(message)
        logger.debug(f"Added message to thread {self.id}: {message}")

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "metadata": self.metadata,
            "chatbot_id": self.chatbot_id,
            "messages": [message.to_dict() for message in self.messages]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Thread':
        thread = cls(
            id=data.get("id", f"thread_{uuid.uuid4().hex[:6]}"),
            created_at=data.get("created_at", int(datetime.now().timestamp())),
            metadata=data.get("metadata", {}),
            chatbot_id=data.get("chatbot_id")
        )
        messages = data.get("messages", [])
        for message_data in messages:
            message = Message.from_dict(message_data)
            thread.add_message(message)
        return thread