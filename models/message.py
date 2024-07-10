from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import logging
from .content_item import ContentItem
from .text_content import TextContent

logger = logging.getLogger(__name__)

@dataclass
class Message:
    role: str
    content: List[ContentItem]
    id: str = field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:6]}")
    created_at: int = field(default_factory=lambda: int(datetime.now().timestamp()))
    thread_id: Optional[str] = None
    chatbot_id: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        return cls(
            role=data['role'],
            content=[ContentItem.from_dict(item) for item in data['content']],
            id=data.get('id'),
            created_at=data.get('created_at'),
            thread_id=data.get('thread_id'),
            chatbot_id=data.get('chatbot_id'),
            metadata=data.get('metadata', {})
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "thread_id": self.thread_id,
            "chatbot_id": self.chatbot_id,
            "role": self.role,
            "content": [
                {
                    "text": {
                        "value": item.text.value,
                        "annotations": item.text.annotations
                    }
                } for item in self.content
            ],
            "metadata": self.metadata
        }
    