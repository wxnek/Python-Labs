import ast
from datetime import datetime

from exceptions import CalculationError
from models import Calculation
from repository import CalculationRepository


class Service:
    """Бизнес-логика калькулятора."""

    def __init__(self, repository: CalculationRepository) -> None:
        self.repository = repository

    def _calculate_expression(self, expression: str) -> float:
        expression = expression.strip()

        if not expression:
            raise CalculationError("Выражение не может быть пустым")

        # Разрешаем только числа и четыре арифметические операции.
        allowed = "0123456789+-*/(). "
        if any(symbol not in allowed for symbol in expression):
            raise CalculationError("Разрешены только числа и операции + - * /")

        if "**" in expression or "//" in expression:
            raise CalculationError("Операции ** и // не поддерживаются")

        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as error:
            raise CalculationError("Некорректное выражение") from error

        for node in ast.walk(tree):
            if not isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp,
                                     ast.Constant, ast.Add, ast.Sub, ast.Mult,
                                     ast.Div, ast.USub, ast.UAdd)):
                raise CalculationError("Недопустимая конструкция в выражении")

            if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
                raise CalculationError("Разрешены только числа")

        try:
            result = eval(compile(tree, "", "eval"), {"__builtins__": {}}, {})
        except ZeroDivisionError as error:
            raise CalculationError("Деление на ноль") from error
        except (TypeError, ValueError, OverflowError) as error:
            raise CalculationError("Не удалось вычислить выражение") from error

        return float(result)

    def calculate(self, expression: str) -> Calculation:
        result = self._calculate_expression(expression)
        calculation = Calculation(
            id=self.repository.get_new_id(),
            expression=expression.strip(),
            result=result,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )
        return self.repository.add(calculation)

    def get_all(self) -> list[Calculation]:
        return self.repository.get_all()

    def get(self, calculation_id: int) -> Calculation:
        calculation = self.repository.get(calculation_id)
        if calculation is None:
            raise CalculationError("Расчёт не найден")
        return calculation

    def update(self, calculation_id: int, expression: str) -> Calculation:
        old = self.get(calculation_id)
        result = self._calculate_expression(expression)
        calculation = Calculation(
            id=old.id,
            expression=expression.strip(),
            result=result,
            timestamp=datetime.now().isoformat(timespec="seconds"),
        )
        self.repository.update(calculation)
        return calculation

    def delete(self, calculation_id: int) -> None:
        if not self.repository.delete(calculation_id):
            raise CalculationError("Расчёт не найден")
