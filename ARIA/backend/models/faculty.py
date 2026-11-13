from dataclasses import dataclass
from backend.models.user import User
@dataclass
class Faculty(User):
    role: str = "faculty"
