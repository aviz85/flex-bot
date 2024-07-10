from dataclasses import dataclass, field
from .text_content import TextContent
from typing import List, Dict, Optional


@dataclass
class ContentItem:
    text: TextContent

    @classmethod
    def from_dict(cls, data: Dict) -> 'ContentItem':
        return cls(
            text=TextContent(
                value=data['text']['value'],
                annotations=data['text'].get('annotations', [])
            )
        )

    def to_dict(self) -> Dict:
        return {
            "text": {
                "value": self.text.value,
                "annotations": self.text.annotations
            }
        }