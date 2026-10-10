from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    available: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
