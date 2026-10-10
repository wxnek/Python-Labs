class Employee:
    """Базовый класс сотрудника."""

    company_name = "TechCompany"

    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

    def get_info(self):
        return f"Сотрудник: {self.name}, возраст: {self.age}, зарплата: {self.salary} руб."

    def change_data(self, name=None, age=None, salary=None):
        if name:
            self.name = name
        if age is not None:
            self.age = age
        if salary is not None:
            self.salary = salary

    def calculate_work_index(self):
        return self.salary

    def show_state(self):
        print(self.get_info())

    def __str__(self):
        return self.get_info()


class Developer(Employee):
    """Класс разработчика."""

    def __init__(self, name, age, salary, programming_language, projects):
        super().__init__(name, age, salary)
        self.programming_language = programming_language
        self.projects = projects

    @property
    def projects(self):
        return self._projects

    @projects.setter
    def projects(self, value):
        if value < 0:
            raise ValueError("Количество проектов не может быть отрицательным.")
        self._projects = value

    def get_info(self):
        return (
            f"Разработчик: {self.name}, возраст: {self.age}, "
            f"зарплата: {self.salary} руб., "
            f"язык: {self.programming_language}, "
            f"проектов: {self.projects}"
        )

    def calculate_work_index(self):
        return self.projects * 10 + self.salary / 10000

    def change_data(
        self, name=None, age=None, salary=None,
        programming_language=None, projects=None
    ):
        super().change_data(name, age, salary)
        if programming_language:
            self.programming_language = programming_language
        if projects is not None:
            self.projects = projects


class Manager(Employee):
    """Класс менеджера."""

    def __init__(self, name, age, salary, subordinates, project_budget):
        super().__init__(name, age, salary)
        self.subordinates = subordinates
        self.project_budget = project_budget

    @property
    def subordinates(self):
        return self._subordinates

    @subordinates.setter
    def subordinates(self, value):
        if value < 0:
            raise ValueError("Количество подчинённых не может быть отрицательным.")
        self._subordinates = value

    @property
    def project_budget(self):
        return self._project_budget

    @project_budget.setter
    def project_budget(self, value):
        if value < 0:
            raise ValueError("Бюджет проектов не может быть отрицательным.")
        self._project_budget = value

    def get_info(self):
        return (
            f"Менеджер: {self.name}, возраст: {self.age}, "
            f"зарплата: {self.salary} руб., "
            f"подчинённых: {self.subordinates}, "
            f"бюджет проектов: {self.project_budget} руб."
        )

    def calculate_work_index(self):
        return self.subordinates * 5 + self.project_budget / 100000

    def change_data(
        self, name=None, age=None, salary=None,
        subordinates=None, project_budget=None
    ):
        super().change_data(name, age, salary)
        if subordinates is not None:
            self.subordinates = subordinates
        if project_budget is not None:
            self.project_budget = project_budget


class Company:
    """Класс компании, содержащий сотрудников."""

    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, index):
        if 0 <= index < len(self.employees):
            removed = self.employees.pop(index)
            print(f"Сотрудник {removed.name} удалён.")
        else:
            print("Сотрудник с таким номером не найден.")

    def show_employees(self):
        if not self.employees:
            print("Список сотрудников пуст.")
            return
        print(f"\n===== СОТРУДНИКИ КОМПАНИИ «{self.name}» =====")
        for i, employee in enumerate(self.employees, start=1):
            print(f"{i}. {employee.get_info()}")

    def execute_work_index(self):
        if not self.employees:
            print("Список сотрудников пуст.")
            return
        print("\n===== РАБОЧИЕ ПОКАЗАТЕЛИ =====")
        for employee in self.employees:
            print(f"{employee.name}: {employee.calculate_work_index():.2f}")

    def show_statistics(self):
        if not self.employees:
            print("Список сотрудников пуст.")
            return
        developers = 0
        managers = 0
        total_salary = 0
        for employee in self.employees:
            total_salary += employee.salary
            if isinstance(employee, Developer):
                developers += 1
            elif isinstance(employee, Manager):
                managers += 1
        average_salary = total_salary / len(self.employees)
        print("\n===== СТАТИСТИКА =====")
        print(f"Всего сотрудников: {len(self.employees)}")
        print(f"Разработчиков: {developers}")
        print(f"Менеджеров: {managers}")
        print(f"Средняя зарплата: {average_salary:.2f} руб.")


def create_employee(company):
    print("\n===== СОЗДАНИЕ СОТРУДНИКА =====")
    print("1. Разработчик")
    print("2. Менеджер")
    employee_type = input("Выберите тип сотрудника: ")
    try:
        name = input("Введите ФИО: ")
        age = int(input("Введите возраст: "))
        salary = float(input("Введите зарплату: "))
        if age <= 0:
            print("Возраст должен быть положительным.")
            return
        if salary < 0:
            print("Зарплата не может быть отрицательной.")
            return
        if employee_type == "1":
            programming_language = input("Введите язык программирования: ")
            projects = int(input("Введите количество проектов: "))
            employee = Developer(name, age, salary, programming_language, projects)
        elif employee_type == "2":
            subordinates = int(input("Введите количество подчинённых: "))
            project_budget = float(input("Введите бюджет проектов: "))
            employee = Manager(name, age, salary, subordinates, project_budget)
        else:
            print("Некорректный тип сотрудника.")
            return
        company.add_employee(employee)
        print("Сотрудник успешно создан.")
    except ValueError as error:
        print(f"Ошибка: {error}")


def edit_employee(company):
    if not company.employees:
        print("Список сотрудников пуст.")
        return
    company.show_employees()
    try:
        index = int(input("Введите номер сотрудника: ")) - 1
        if not (0 <= index < len(company.employees)):
            print("Сотрудник с таким номером не найден.")
            return
        employee = company.employees[index]
        print("\nВведите новые значения.")
        print("Для сохранения текущего значения оставьте поле пустым.")
        name = input(f"ФИО [{employee.name}]: ")
        age_input = input(f"Возраст [{employee.age}]: ")
        salary_input = input(f"Зарплата [{employee.salary}]: ")
        age = int(age_input) if age_input else None
        salary = float(salary_input) if salary_input else None
        if isinstance(employee, Developer):
            language = input(f"Язык программирования [{employee.programming_language}]: ")
            projects_input = input(f"Количество проектов [{employee.projects}]: ")
            projects = int(projects_input) if projects_input else None
            employee.change_data(name=name or None, age=age, salary=salary,
                                 programming_language=language or None, projects=projects)
        elif isinstance(employee, Manager):
            subordinates_input = input(f"Количество подчинённых [{employee.subordinates}]: ")
            budget_input = input(f"Бюджет проектов [{employee.project_budget}]: ")
            subordinates = int(subordinates_input) if subordinates_input else None
            project_budget = float(budget_input) if budget_input else None
            employee.change_data(name=name or None, age=age, salary=salary,
                                 subordinates=subordinates, project_budget=project_budget)
        print("Данные сотрудника успешно изменены.")
    except ValueError as error:
        print(f"Ошибка: {error}")


def show_employee_state(company):
    if not company.employees:
        print("Список сотрудников пуст.")
        return
    company.show_employees()
    try:
        index = int(input("Введите номер сотрудника: ")) - 1
        if 0 <= index < len(company.employees):
            company.employees[index].show_state()
        else:
            print("Сотрудник с таким номером не найден.")
    except ValueError:
        print("Необходимо ввести целое число.")


def test_property():
    print("\n===== ТЕСТ PROPERTY =====")
    employee = Developer("Тестовый сотрудник", 25, 80000, "Python", 3)
    print(f"Количество проектов: {employee.projects}")
    try:
        employee.projects = -1
    except ValueError as error:
        print(f"Ошибка при изменении значения: {error}")


def main():
    company = Company("TechCompany")
    company.add_employee(Developer("Иванов Иван Иванович", 25, 120000, "Python", 5))
    company.add_employee(Manager("Петров Пётр Петрович", 35, 150000, 8, 2000000))
    company.add_employee(Developer("Сидоров Алексей Сергеевич", 28, 130000, "C++", 7))

    while True:
        print("\n===================================")
        print("        СИСТЕМА УЧЁТА СОТРУДНИКОВ")
        print("===================================")
        print("1. Создать объект")
        print("2. Показать объекты")
        print("3. Рассчитать рабочий показатель")
        print("4. Изменить объект")
        print("5. Удалить объект")
        print("6. Показать статистику")
        print("7. Показать состояние объекта")
        print("8. Проверить property")
        print("0. Выход")
        choice = input("Выберите пункт меню: ")
        if choice == "1":
            create_employee(company)
        elif choice == "2":
            company.show_employees()
        elif choice == "3":
            company.execute_work_index()
        elif choice == "4":
            edit_employee(company)
        elif choice == "5":
            company.show_employees()
            try:
                index = int(input("Введите номер сотрудника для удаления: ")) - 1
                company.remove_employee(index)
            except ValueError:
                print("Необходимо ввести целое число.")
        elif choice == "6":
            company.show_statistics()
        elif choice == "7":
            show_employee_state(company)
        elif choice == "8":
            test_property()
        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Некорректный пункт меню.")


if __name__ == "__main__":
    main()
