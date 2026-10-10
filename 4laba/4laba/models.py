from exceptions import NegativeSalaryError


class Employee:
    def __init__(self, name, position, department, salary):
        self.name = name
        self.position = position
        self.department = department
        self.set_salary(salary)

    def set_salary(self, salary):
        if salary < 0:
            raise NegativeSalaryError("Зарплата не может быть отрицательной")
        self.salary = salary

    def to_dict(self):
        return {
            "name": self.name,
            "position": self.position,
            "department": self.department,
            "salary": self.salary
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["position"],
            data["department"],
            data["salary"]
        )
