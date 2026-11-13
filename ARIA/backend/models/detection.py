from dataclasses import dataclass
@dataclass
class Detection:
    id: int; label: str; photo: str = ""; kind: str = "usage"; created_at: str = ""
