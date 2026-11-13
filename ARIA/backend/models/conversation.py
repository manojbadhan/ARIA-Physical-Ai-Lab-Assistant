from dataclasses import dataclass
@dataclass
class Message:
    id: int; user_id: int; role: str; text: str; created_at: str = ""
