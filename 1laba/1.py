def calculate_average(salaries):
    total = 0
    for salary in salaries:
        total += salary
    return total / len(salaries)
def count_above_average(salaries, average):
    count = 0
    for salary in salaries:
        if salary > average:
            count += 1
    return count
def determine_category(average):
    if average < 30000:
        return "Низкий уровень зарплаты"
    elif average < 60000:
        return "Средний уровень зарплаты"
    else:
        return "Высокий уровень зарплаты"
def main():
    print("Анализ заработной платы сотрудников")
    print()
    count = int(input("Введите количество сотрудников: "))
    if count <= 0:
        print("Ошибка: количество сотрудников должно быть больше нуля.")
        return
    salaries = []
    for i in range(count):
        salary = float(input(f"Введите зарплату сотрудника {i + 1}: "))
        if salary < 0:
            print("Ошибка: зарплата не может быть отрицательной.")
            return
        salaries.append(salary)
    average = calculate_average(salaries)
    maximum = max(salaries)
    minimum = min(salaries)
    above_average = count_above_average(salaries, average)
    total_salary = sum(salaries)
    category = determine_category(average)
    print("\nРезультаты анализа:")
    print(f"Средняя зарплата: {average:.2f} руб.")
    print(f"Максимальная зарплата: {maximum:.2f} руб.")
    print(f"Минимальная зарплата: {minimum:.2f} руб.")
    print(f"Сотрудников с зарплатой выше средней: {above_average}")
    print(f"Фонд заработной платы: {total_salary:.2f} руб.")
    print(f"Категория средней зарплаты: {category}")
if __name__ == "__main__":
    main()
6