from exceptions import EmployeeNotFoundError


def add_employee(employees, employee):
    employees.append(employee)


def find_employee(employees, name):
    for employee in employees:
        if employee.name.lower() == name.lower():
            return employee
    raise EmployeeNotFoundError("Сотрудник не найден")


def change_salary(employees, name, new_salary):
    employee = find_employee(employees, name)
    employee.set_salary(new_salary)


def delete_employee(employees, name):
    employee = find_employee(employees, name)
    employees.remove(employee)


def get_salary_statistics(employees):
    if len(employees) == 0:
        return None

    salaries = []
    for employee in employees:
        salaries.append(employee.salary)

    average = sum(salaries) / len(salaries)
    maximum = max(salaries)
    minimum = min(salaries)

    return average, maximum, minimum
