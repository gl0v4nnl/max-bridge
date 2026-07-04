from dataclasses import dataclass


@dataclass(slots=True)
class Message:
    sender: str
    text: str
    time: str
    direction: str = "unknown"  # incoming / outgoing