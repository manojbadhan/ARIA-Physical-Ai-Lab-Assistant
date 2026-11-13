from dataclasses import dataclass
from typing import Optional
@dataclass
class Equipment:
    id: int; name: str; location: str; qty: int; photo: Optional[str] = None; updated_at: str = ""
