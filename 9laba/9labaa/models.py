from dataclasses import dataclass


@dataclass
class Calculation:
    id: int
    expression: str
    result: float
    timestamp: str
