from dataclasses import dataclass, field
from typing import List

@dataclass
class TextContent:
    value: str
    annotations: List = field(default_factory=list)