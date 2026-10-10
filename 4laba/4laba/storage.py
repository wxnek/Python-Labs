import csv
import json
import os

from models import Employee
from exceptions import NegativeSalaryError

DATA_DIR = "data"
JSON_FILE = os.path.join(DATA_DIR, "employees.json")
CSV_FILE = os.path.join(DATA_DIR, "employees.csv")


def save_json(employees):
    os.makedirs(DATA_DIR, exist_ok=True)

    data = []
    for employee in employees:
        data.append(employee.to_dict())

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_json():
    if not os.path.exists(JSON_FILE):
        return []

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список сотрудников")

        employees = []
        for item in data:
            employees.append(Employee.from_dict(item))

        return employees

    except json.JSONDecodeError:
        raise ValueError("JSON-файл содержит некорректные данные")
    except (KeyError, TypeError, ValueError, NegativeSalaryError):
        raise ValueError("JSON-файл имеет неверную структуру")


def export_csv(employees):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(CSV_FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["name", "position", "department", "salary"]
        )
        writer.writeheader()

        for employee in employees:
            writer.writerow(employee.to_dict())
