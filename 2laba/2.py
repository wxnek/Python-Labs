
def add_employee(employees):
    print("\n--- Добавление сотрудника ---")
    name = input("ФИО: ").strip()
    position = input("Должность: ").strip()
    department = input("Отдел: ").strip()
    while True:
        try:
            salary = float(input("Зарплата: "))
            if salary < 0:
                print("Зарплата не может быть отрицательной.")
            else:
                break
        except ValueError:
            print("Введите число.")
    employee = {
        "name": name,
        "position": position,
        "department": department,
        "salary": salary
    }
    employees.append(employee)
    print("Сотрудник добавлен.")
def show_employees(employees):
    print("\n--- Список сотрудников ---")
    if not employees:
        print("Список сотрудников пуст.")
        return
    for i, employee in enumerate(employees, 1):
        print(
            f"{i}. {employee['name']} | "
            f"{employee['position']} | "
            f"{employee['department']} | "
            f"{employee['salary']:.2f} руб."
        )
def find_by_department(employees, department):
    result = []
    for employee in employees:
        if employee["department"].lower() == department.lower():
            result.append(employee)

    return result
def filter_by_salary(employees, minimum_salary):
    result = [
        employee
        for employee in employees
        if employee["salary"] >= minimum_salary
    ]

    return result
def calculate_average_salary(employees):
    if not employees:
        return 0
    total_salary = 0
    for employee in employees:
        total_salary += employee["salary"]
    return total_salary / len(employees)
def find_highest_paid(employees):
    if not employees:
        return None
    highest = employees[0]
    for employee in employees:
        if employee["salary"] > highest["salary"]:
            highest = employee
    return highest
def get_unique_positions(employees):
    positions = set()
    for employee in employees:
        positions.add(employee["position"])
    return positions
def sort_by_salary(employees):
    return sorted(employees, key=lambda employee: employee["salary"])
def show_statistics(employees):
    print("\n--- Статистика ---")
    if not employees:
        print("Нет данных для статистики.")
        return
    average_salary = calculate_average_salary(employees)
    highest_paid = find_highest_paid(employees)
    total_salary = sum(employee["salary"] for employee in employees)
    minimum_salary = min(employee["salary"] for employee in employees)
    maximum_salary = max(employee["salary"] for employee in employees)
    print(f"Количество сотрудников: {len(employees)}")
    print(f"Средняя зарплата: {average_salary:.2f} руб.")
    print(f"Общая сумма зарплат: {total_salary:.2f} руб.")
    print(f"Минимальная зарплата: {minimum_salary:.2f} руб.")
    print(f"Максимальная зарплата: {maximum_salary:.2f} руб.")
    print(
        f"Самый высокооплачиваемый сотрудник: "
        f"{highest_paid['name']} — {highest_paid['salary']:.2f} руб."
    )
def show_employee_list(employees):
    if not employees:
        print("Подходящих сотрудников не найдено.")
        return
    for i, employee in enumerate(employees, 1):
        print(
            f"{i}. {employee['name']} | "
            f"{employee['position']} | "
            f"{employee['department']} | "
            f"{employee['salary']:.2f} руб."
        )
def main():
    employees = []
    while True:
        print("\n===== МЕНЮ =====")
        print("1. Добавить сотрудника")
        print("2. Показать всех сотрудников")
        print("3. Найти сотрудников по отделу")
        print("4. Фильтрация по зарплате")
        print("5. Сортировка по зарплате")
        print("6. Статистика")
        print("7. Уникальные должности")
        print("0. Выход")
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            show_employees(employees)
        elif choice == "3":
            if not employees:
                print("Список сотрудников пуст.")
                continue
            department = input("Введите название отдела: ").strip()
            result = find_by_department(employees, department)
            print(f"\n--- Сотрудники отдела '{department}' ---")
            show_employee_list(result)
        elif choice == "4":
            if not employees:
                print("Список сотрудников пуст.")
                continue
            while True:
                try:
                    minimum_salary = float(
                        input("Введите минимальную зарплату: ")
                    )
                    if minimum_salary < 0:
                        print("Зарплата не может быть отрицательной.")
                    else:
                        break
                except ValueError:
                    print("Введите число.")
            result = filter_by_salary(employees, minimum_salary)
            print(
                f"\n--- Сотрудники с зарплатой "
                f"от {minimum_salary:.2f} руб. ---"
            )
            show_employee_list(result)
        elif choice == "5":
            if not employees:
                print("Список сотрудников пуст.")
                continue
            sorted_employees = sort_by_salary(employees)
            print("\n--- Сотрудники по возрастанию зарплаты ---")
            show_employee_list(sorted_employees)
        elif choice == "6":
            show_statistics(employees)
        elif choice == "7":
            if not employees:
                print("Список сотрудников пуст.")
                continue
            positions = get_unique_positions(employees)
            print("\n--- Уникальные должности ---")
            for position in sorted(positions):
                print("-", position)
        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Неверный пункт меню. Попробуйте ещё раз.")
if __name__ == "__main__":
    main()

