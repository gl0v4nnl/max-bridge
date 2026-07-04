from dataclasses import dataclass

@dataclass(slots=True)
class ChatInfo:
    title: str
    author: str
    preview: str
    time: str