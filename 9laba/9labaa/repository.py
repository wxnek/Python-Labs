import threading
from typing import Optional

from models import Calculation


class CalculationRepository:
    """Хранит расчёты в памяти программы."""

    def __init__(self) -> None:
        self.calculations: dict[int, Calculation] = {}
        self.next_id = 1
        self.lock = threading.Lock()

    def add(self, calculation: Calculation) -> Calculation:
        with self.lock:
            self.calculations[calculation.id] = calculation
        return calculation

    def get(self, calculation_id: int) -> Optional[Calculation]:
        with self.lock:
            return self.calculations.get(calculation_id)

    def get_all(self) -> list[Calculation]:
        with self.lock:
            return list(self.calculations.values())

    def update(self, calculation: Calculation) -> bool:
        with self.lock:
            if calculation.id not in self.calculations:
                return False
            self.calculations[calculation.id] = calculation
            return True

    def delete(self, calculation_id: int) -> bool:
        with self.lock:
            if calculation_id not in self.calculations:
                return False
            del self.calculations[calculation_id]
            return True

    def get_new_id(self) -> int:
        with self.lock:
            calculation_id = self.next_id
            self.next_id += 1
            return calculation_id
