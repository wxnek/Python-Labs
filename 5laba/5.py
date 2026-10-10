


class Employee:
    def __init__(self, name, department, position, salary):
        self.name = name
        self.department = department
        self.position = position
        self.salary = salary

    def __str__(self):
        return f"{self.name} | {self.department} | {self.position} | {self.salary} руб."


# Первый производный класс
class Manager(Employee):
    def __init__(self, name, department, salary):
        super().__init__(name, department, "Менеджер", salary)


# Второй производный класс
class Developer(Employee):
    def __init__(self, name, department, salary):
        super().__init__(name, department, "Разработчик", salary)


# Функция высшего порядка для фильтрации
def filter_objects(objects, condition):
    return list(filter(condition, objects))


# Функция высшего порядка для преобразования данных
def transform_objects(objects, operation):
    return list(map(operation, objects))


# Функция высшего порядка для сортировки
def sort_objects(objects, key_function):
    return sorted(objects, key=key_function)


# Генератор сотрудников выбранного отдела
def employees_by_department(objects, department):
    for employee in objects:
        if employee.department == department:
            yield employee


def main():
    # Создаём список сотрудников
    employees = [
        Manager("Иванов Иван", "Продажи", 85000),
        Developer("Петров Пётр", "IT", 120000),
        Developer("Сидоров Алексей", "IT", 95000),
        Manager("Смирнова Анна", "Продажи", 100000),
        Developer("Кузнецов Дмитрий", "IT", 110000)
    ]

    print("===== Список сотрудников =====")
    for employee in employees:
        print(employee)

    # ---------------------------------------
    # 1. Фильтрация по зарплате
    # ---------------------------------------
    try:
        minimum_salary = float(
            input("\nВведите минимальную зарплату: ")
        )

        if minimum_salary < 0:
            raise ValueError("Зарплата не может быть отрицательной")

        high_salary = filter_objects(
            employees,
            lambda employee: employee.salary >= minimum_salary
        )

        print("\nСотрудники с указанной зарплатой и выше:")
        for employee in high_salary:
            print(employee)

    except ValueError as error:
        print("Ошибка:", error)

    # ---------------------------------------
    # 2. Получение списка должностей через map()
    # ---------------------------------------
    positions = transform_objects(
        employees,
        lambda employee: employee.position
    )

    print("\nСписок должностей:")
    print(positions)

    # ---------------------------------------
    # 3. Сортировка по зарплате
    # ---------------------------------------
    sorted_employees = sort_objects(
        employees,
        lambda employee: employee.salary
    )

    print("\nСотрудники по возрастанию зарплаты:")
    for employee in sorted_employees:
        print(employee)

    # ---------------------------------------
    # 4. Самый высокооплачиваемый сотрудник
    # ---------------------------------------
    highest_paid = max(
        employees,
        key=lambda employee: employee.salary
    )

    print("\nСамый высокооплачиваемый сотрудник:")
    print(highest_paid)

    # ---------------------------------------
    # 5. Проверка наличия сотрудников отдела
    # ---------------------------------------
    department = input(
        "\nВведите отдел для проверки: "
    )

    has_department = any(
        employee.department == department
        for employee in employees
    )

    if has_department:
        print("В таком отделе есть сотрудники.")
    else:
        print("Сотрудников такого отдела нет.")

    # ---------------------------------------
    # 6. Генератор сотрудников отдела
    # ---------------------------------------
    print("\nСотрудники выбранного отдела:")

    found = False

    for employee in employees_by_department(
        employees,
        department
    ):
        print(employee)
        found = True

    if not found:
        print("Нет сотрудников в этом отделе.")

    # ---------------------------------------
    # 7. List comprehension
    # ---------------------------------------
    names = [employee.name for employee in employees]

    print("\nФИО всех сотрудников:")
    print(names)

    # ---------------------------------------
    # 8. Дополнительная проверка через all()
    # ---------------------------------------
    all_have_salary = all(
        employee.salary > 0
        for employee in employees
    )

    print("\nУ всех сотрудников зарплата больше нуля:", all_have_salary)


if __name__ == "__main__":
    main()
