class NegativeSalaryError(Exception):
    """Ошибка при попытке установить отрицательную зарплату."""
    pass


class EmployeeNotFoundError(Exception):
    """Сотрудник не найден."""
    pass
