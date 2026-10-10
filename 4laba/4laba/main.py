from exceptions import EmployeeNotFoundError, NegativeSalaryError
from models import Employee
from services import (
    add_employee,
    change_salary,
    delete_employee,
    find_employee,
    get_salary_statistics,
)
from storage import export_csv, load_json, save_json


def read_salary():
    while True:
        try:
            return float(input("Зарплата: "))
        except ValueError:
            print("Ошибка: введите число")


def show_employees(employees):
    if len(employees) == 0:
        print("Список сотрудников пуст.")
        return

    for number, employee in enumerate(employees, 1):
        print(
            f"{number}. {employee.name} | {employee.position} | "
            f"{employee.department} | {employee.salary:.2f}"
        )


def add_new_employee(employees):
    name = input("ФИО: ")
    position = input("Должность: ")
    department = input("Отдел: ")
    salary = read_salary()

    try:
        employee = Employee(name, position, department, salary)
        add_employee(employees, employee)
        save_json(employees)
        print("Сотрудник добавлен.")
    except NegativeSalaryError as error:
        print(f"Ошибка: {error}")


def search_employee(employees):
    name = input("Введите ФИО для поиска: ")

    try:
        employee = find_employee(employees, name)
        print("Сотрудник найден:")
        print(f"ФИО: {employee.name}")
        print(f"Должность: {employee.position}")
        print(f"Отдел: {employee.department}")
        print(f"Зарплата: {employee.salary:.2f}")
    except EmployeeNotFoundError as error:
        print(f"Ошибка: {error}")


def change_employee_salary(employees):
    name = input("Введите ФИО: ")
    new_salary = read_salary()

    try:
        change_salary(employees, name, new_salary)
        save_json(employees)
        print("Зарплата изменена.")
    except EmployeeNotFoundError as error:
        print(f"Ошибка: {error}")
    except NegativeSalaryError as error:
        print(f"Ошибка: {error}")


def remove_employee(employees):
    name = input("Введите ФИО для удаления: ")

    try:
        delete_employee(employees, name)
        save_json(employees)
        print("Сотрудник удалён.")
    except EmployeeNotFoundError as error:
        print(f"Ошибка: {error}")


def show_statistics(employees):
    statistics = get_salary_statistics(employees)

    if statistics is None:
        print("Нет данных для расчёта статистики.")
        return

    average, maximum, minimum = statistics
    print(f"Средняя зарплата: {average:.2f}")
    print(f"Максимальная зарплата: {maximum:.2f}")
    print(f"Минимальная зарплата: {minimum:.2f}")


def main():
    try:
        employees = load_json()
    except ValueError as error:
        print(f"Ошибка загрузки: {error}")
        employees = []

    while True:
        print("\n===== УЧЁТ СОТРУДНИКОВ =====")
        print("1. Добавить сотрудника")
        print("2. Показать всех сотрудников")
        print("3. Найти сотрудника")
        print("4. Изменить зарплату")
        print("5. Удалить сотрудника")
        print("6. Показать статистику зарплат")
        print("7. Сохранить JSON")
        print("8. Экспортировать CSV")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            add_new_employee(employees)
        elif choice == "2":
            show_employees(employees)
        elif choice == "3":
            search_employee(employees)
        elif choice == "4":
            change_employee_salary(employees)
        elif choice == "5":
            remove_employee(employees)
        elif choice == "6":
            show_statistics(employees)
        elif choice == "7":
            save_json(employees)
            print("Данные сохранены в JSON.")
        elif choice == "8":
            export_csv(employees)
            print("Данные экспортированы в CSV.")
        elif choice == "0":
            save_json(employees)
            print("Программа завершена.")
            break
        else:
            print("Ошибка: неизвестный пункт меню.")


if __name__ == "__main__":
    main()
