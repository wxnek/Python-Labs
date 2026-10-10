from dataclasses import dataclass
from enum import Enum
from functools import wraps
from contextlib import contextmanager
from typing import Protocol
from datetime import date, datetime
import inspect
import time


# ==================== ИСКЛЮЧЕНИЯ ====================

class LibraryError(Exception):
    pass


class ItemNotFoundError(LibraryError):
    pass


class InvalidOperationError(LibraryError):
    pass


# ==================== ENUM ====================

class Status(Enum):
    AVAILABLE = "доступно"
    ISSUED = "выдано"
    RESERVED = "зарезервировано"


# ==================== МОДЕЛИ ====================

@dataclass
class LibraryItem:
    item_id: int
    title: str
    status: Status = Status.AVAILABLE

    def get_report(self) -> str:
        return f"#{self.item_id}: {self.title}, статус: {self.status.value}"


@dataclass
class Book(LibraryItem):
    author: str = ""
    pages: int = 0

    def get_report(self) -> str:
        return (
            f"Книга #{self.item_id}: {self.title}; "
            f"автор: {self.author}; страниц: {self.pages}; "
            f"статус: {self.status.value}"
        )


@dataclass
class Journal(LibraryItem):
    issue_number: int = 0
    year: int = 0

    def get_report(self) -> str:
        return (
            f"Журнал #{self.item_id}: {self.title}; "
            f"№ выпуска: {self.issue_number}; год: {self.year}; "
            f"статус: {self.status.value}"
        )


@dataclass
class ElectronicEdition(LibraryItem):
    file_format: str = "PDF"
    size_mb: float = 0.0

    def get_report(self) -> str:
        return (
            f"Электронное издание #{self.item_id}: {self.title}; "
            f"формат: {self.file_format}; размер: {self.size_mb:.1f} МБ; "
            f"статус: {self.status.value}"
        )


@dataclass
class Loan:
    item_id: int
    reader: str
    issue_date: date
    due_date: date
    returned: bool = False


# ==================== ДЕКОРАТОРЫ ====================

# Декоратор №1 — журналирование
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Вызов: {func.__name__}()")
        result = func(*args, **kwargs)
        return result

    return wrapper


# Декоратор №2 — измерение времени
def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start
        print(
            f"[PERFORMANCE] {func.__name__}: "
            f"{elapsed:.6f} сек"
        )

        return result

    return wrapper


# Декоратор №3 — декоратор с параметром
def repeat(count: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(count):
                func(*args, **kwargs)

        return wrapper

    return decorator


@repeat(2)
def decorator_demo():
    print("Декоратор с параметром работает")


# ==================== КОНТЕКСТНЫЙ МЕНЕДЖЕР ====================

class LibraryOperation:

    def __enter__(self):
        print("[CONTEXT] Начало операции")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print("[CONTEXT] Операция завершена")
        else:
            print(f"[CONTEXT] Ошибка: {exc_value}")

        return False


# ==================== PROTOCOL ====================

class Reportable(Protocol):

    def get_report(self) -> str:
        ...


def print_report(obj: Reportable) -> None:
    print(obj.get_report())


# ==================== БИБЛИОТЕКА ====================

class Library:

    def __init__(self) -> None:
        self.items: list[LibraryItem] = []
        self.loans: list[Loan] = []

    # Добавление
    @log_call
    def add_item(self, item: LibraryItem) -> None:

        for existing in self.items:
            if existing.item_id == item.item_id:
                raise LibraryError(
                    "Издание с таким ID уже существует"
                )

        self.items.append(item)

    # Удаление
    @log_call
    def remove_item(self, item_id: int) -> None:

        item = self.find_item(item_id)

        if item.status == Status.ISSUED:
            raise InvalidOperationError(
                "Нельзя удалить выданное издание"
            )

        self.items.remove(item)

    # Поиск
    @log_call
    def find_item(self, item_id: int) -> LibraryItem:

        for item in self.items:

            if item.item_id == item_id:
                return item

        raise ItemNotFoundError(
            "Издание не найдено"
        )

    # Резервирование
    @log_call
    def reserve_item(self, item_id: int) -> None:

        item = self.find_item(item_id)

        if item.status != Status.AVAILABLE:
            raise InvalidOperationError(
                "Зарезервировать можно только "
                "доступное издание"
            )

        item.status = Status.RESERVED

    # Отмена резервирования
    @log_call
    def cancel_reservation(self, item_id: int) -> None:

        item = self.find_item(item_id)

        if item.status != Status.RESERVED:
            raise InvalidOperationError(
                "Издание не находится в резерве"
            )

        item.status = Status.AVAILABLE

    # Выдача
    @log_call
    def issue_item(
        self,
        item_id: int,
        reader: str,
        due_date: date
    ) -> None:

        item = self.find_item(item_id)

        if item.status != Status.AVAILABLE:
            raise InvalidOperationError(
                "Выдать можно только доступное издание"
            )

        if due_date < date.today():
            raise InvalidOperationError(
                "Дата возврата не может быть в прошлом"
            )

        item.status = Status.ISSUED

        loan = Loan(
            item_id=item_id,
            reader=reader,
            issue_date=date.today(),
            due_date=due_date
        )

        self.loans.append(loan)

    # Возврат
    @log_call
    def return_item(self, item_id: int) -> None:

        item = self.find_item(item_id)

        if item.status != Status.ISSUED:
            raise InvalidOperationError(
                "Издание сейчас не выдано"
            )

        for loan in self.loans:

            if loan.item_id == item_id and not loan.returned:
                loan.returned = True
                item.status = Status.AVAILABLE
                return

        raise LibraryError(
            "Активная выдача не найдена"
        )

    # Поиск просроченных выдач
    def overdue_loans(self) -> list[Loan]:

        today = date.today()

        overdue = []

        for loan in self.loans:

            if not loan.returned and loan.due_date < today:
                overdue.append(loan)

        return overdue

    # Статистика
    @measure_time
    def statistics(self) -> None:

        total = len(self.items)

        available = 0
        issued = 0
        reserved = 0

        for item in self.items:

            if item.status == Status.AVAILABLE:
                available += 1

            elif item.status == Status.ISSUED:
                issued += 1

            elif item.status == Status.RESERVED:
                reserved += 1

        print()
        print("=== СТАТИСТИКА ===")
        print(f"Всего изданий: {total}")
        print(f"Доступно: {available}")
        print(f"Выдано: {issued}")
        print(f"Зарезервировано: {reserved}")
        print(
            "Активных просроченных выдач: "
            f"{len(self.overdue_loans())}"
        )


# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def read_int(
    prompt: str,
    minimum: int | None = None
) -> int:

    while True:

        try:
            value = int(input(prompt))

            if minimum is not None and value < minimum:
                print(
                    f"Введите число не меньше {minimum}"
                )
                continue

            return value

        except ValueError:
            print(
                "Ошибка: введите целое число"
            )


def read_float(
    prompt: str,
    minimum: float | None = None
) -> float:

    while True:

        try:
            value = float(input(prompt))

            if minimum is not None and value < minimum:
                print(
                    f"Введите число не меньше {minimum}"
                )
                continue

            return value

        except ValueError:
            print("Ошибка: введите число")


def read_date(prompt: str) -> date:

    while True:

        value = input(prompt)

        try:
            return datetime.strptime(
                value,
                "%d.%m.%Y"
            ).date()

        except ValueError:
            print(
                "Ошибка: используйте формат "
                "ДД.ММ.ГГГГ"
            )


# ==================== ДОБАВЛЕНИЕ ИЗДАНИЯ ====================

def add_item_from_input(library: Library) -> None:

    print()
    print("1. Книга")
    print("2. Журнал")
    print("3. Электронное издание")

    item_type = read_int(
        "Выберите тип: ",
        1
    )

    if item_type not in (1, 2, 3):
        raise ValueError(
            "Такого типа нет"
        )

    item_id = read_int(
        "ID: ",
        1
    )

    title = input(
        "Название: "
    ).strip()

    if not title:
        raise ValueError(
            "Название не может быть пустым"
        )

    # Книга
    if item_type == 1:

        author = input(
            "Автор: "
        ).strip()

        pages = read_int(
            "Количество страниц: ",
            1
        )

        item = Book(
            item_id,
            title,
            Status.AVAILABLE,
            author,
            pages
        )

    # Журнал
    elif item_type == 2:

        issue_number = read_int(
            "Номер выпуска: ",
            1
        )

        year = read_int(
            "Год выпуска: ",
            1
        )

        item = Journal(
            item_id,
            title,
            Status.AVAILABLE,
            issue_number,
            year
        )

    # Электронное издание
    else:

        file_format = input(
            "Формат файла: "
        ).strip()

        size_mb = read_float(
            "Размер файла (МБ): ",
            0
        )

        item = ElectronicEdition(
            item_id,
            title,
            Status.AVAILABLE,
            file_format,
            size_mb
        )

    library.add_item(item)

    print("Издание добавлено")


# ==================== ВЫВОД ВСЕХ ИЗДАНИЙ ====================

def show_all(library: Library) -> None:

    if not library.items:
        print("Библиотека пуста")
        return

    print()
    print("=== ВСЕ ИЗДАНИЯ ===")

    for item in library.items:
        print_report(item)


# ==================== ИНТРОСПЕКЦИЯ ====================

def inspect_item(item: LibraryItem) -> None:

    print()
    print("=== ИНТРОСПЕКЦИЯ ===")

    # type()
    print(
        "Тип:",
        type(item).__name__
    )

    # isinstance()
    print(
        "Является LibraryItem:",
        isinstance(item, LibraryItem)
    )

    # issubclass()
    print(
        "Book является LibraryItem:",
        issubclass(Book, LibraryItem)
    )

    # hasattr()
    print(
        "Есть атрибут title:",
        hasattr(item, "title")
    )

    # getattr()
    print(
        "Название через getattr:",
        getattr(item, "title")
    )

    # dir()
    public_members = [
        name
        for name in dir(item)
        if not name.startswith("_")
    ]

    print(
        "Открытые элементы:",
        ", ".join(public_members)
    )

    # inspect.signature()
    print(
        "Сигнатура get_report:",
        inspect.signature(item.get_report)
    )


# ==================== МЕНЮ ====================

def menu() -> None:

    library = Library()

    while True:

        print()
        print("===== БИБЛИОТЕКА =====")
        print("1. Добавить издание")
        print("2. Удалить издание")
        print("3. Найти издание")
        print("4. Показать все издания")
        print("5. Зарезервировать издание")
        print("6. Выдать издание")
        print("7. Вернуть издание")
        print("8. Найти просроченные выдачи")
        print("9. Показать статистику")
        print("10. Интроспекция объекта")
        print("11. Демонстрация декораторов")
        print("12. Демонстрация контекстного менеджера")
        print("13. Демонстрация Protocol")
        print("0. Выход")

        choice = input(
            "Выберите пункт: "
        )

        try:

            # Добавить
            if choice == "1":
                add_item_from_input(library)

            # Удалить
            elif choice == "2":

                item_id = read_int(
                    "ID издания: ",
                    1
                )

                library.remove_item(item_id)

                print("Издание удалено")

            # Найти
            elif choice == "3":

                item_id = read_int(
                    "ID издания: ",
                    1
                )

                item = library.find_item(
                    item_id
                )

                print_report(item)

            # Показать все
            elif choice == "4":
                show_all(library)

            # Зарезервировать
            elif choice == "5":

                item_id = read_int(
                    "ID издания: ",
                    1
                )

                library.reserve_item(
                    item_id
                )

                print(
                    "Издание зарезервировано"
                )

            # Выдать
            elif choice == "6":

                item_id = read_int(
                    "ID издания: ",
                    1
                )

                reader = input(
                    "ФИО читателя: "
                ).strip()

                if not reader:
                    raise ValueError(
                        "ФИО не может быть пустым"
                    )

                due_date = read_date(
                    "Дата возврата (ДД.ММ.ГГГГ): "
                )

                with LibraryOperation():
                    library.issue_item(
                        item_id,
                        reader,
                        due_date
                    )

                print("Издание выдано")

            # Вернуть
            elif choice == "7":

                item_id = read_int(
                    "ID издания: ",
                    1
                )

                with LibraryOperation():
                    library.return_item(
                        item_id
                    )

                print("Издание возвращено")

            # Просроченные выдачи
            elif choice == "8":

                overdue = library.overdue_loans()

                if not overdue:
                    print(
                        "Просроченных выдач нет"
                    )

                else:

                    print()
                    print(
                        "=== ПРОСРОЧЕННЫЕ ВЫДАЧИ ==="
                    )

                    for loan in overdue:

                        print(
                            f"ID: {loan.item_id}; "
                            f"читатель: {loan.reader}; "
                            f"выдать до: "
                            f"{loan.due_date.strftime('%d.%m.%Y')}"
                        )

            # Статистика
            elif choice == "9":
                library.statistics()

            # Интроспекция
            elif choice == "10":

                item_id = read_int(
                    "ID издания: ",
                    1
                )

                item = library.find_item(
                    item_id
                )

                inspect_item(item)

            # Декораторы
            elif choice == "11":

                print(
                    "Обычный декоратор @log_call "
                    "срабатывает при вызове методов библиотеки."
                )

                print(
                    "Декоратор @measure_time "
                    "срабатывает при расчёте статистики."
                )

                print(
                    "Декоратор с параметром @repeat:"
                )

                decorator_demo()

            # Context manager
            elif choice == "12":

                with LibraryOperation():

                    print(
                        "Внутри блока with выполняется "
                        "операция библиотеки"
                    )

            # Protocol
            elif choice == "13":

                if not library.items:

                    print(
                        "Сначала добавьте хотя бы "
                        "одно издание"
                    )

                else:

                    reportable: Reportable = (
                        library.items[0]
                    )

                    print_report(
                        reportable
                    )

                    print(
                        "Protocol Reportable "
                        "успешно использован"
                    )

            # Выход
            elif choice == "0":

                print(
                    "Программа завершена"
                )

                break

            else:

                print(
                    "Ошибка: такого пункта меню нет"
                )

        except LibraryError as error:

            print(
                f"Ошибка библиотеки: {error}"
            )

        except ValueError as error:

            print(
                f"Ошибка ввода: {error}"
            )


# ==================== ЗАПУСК ====================

if __name__ == "__main__":
    menu()