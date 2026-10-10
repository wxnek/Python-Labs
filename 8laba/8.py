from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable


# -------------------- МОДЕЛЬ --------------------

class BookStatus(Enum):
    AVAILABLE = "свободна"
    LOANED = "выдана"
    RESERVED = "забронирована"


class BookType(Enum):
    PRINTED = "1"
    ELECTRONIC = "2"
    MAGAZINE = "3"


@dataclass
class Book:
    id: int
    title: str
    author: str
    status: BookStatus = BookStatus.AVAILABLE
    reader: str = ""
    loan_days: int = 0


@dataclass
class PrintedBook(Book):
    pass


@dataclass
class ElectronicBook(Book):
    pass


@dataclass
class Magazine(Book):
    pass


# -------------------- REPOSITORY --------------------

@runtime_checkable
class Repository(Protocol):
    def add(self, entity: Book):
        ...

    def get(self, entity_id: int):
        ...

    def get_all(self):
        ...

    def delete(self, entity_id: int):
        ...


class InMemoryRepository:
    """Хранит книги в памяти программы."""

    def __init__(self):
        self.books = {}

    def add(self, entity: Book):
        self.books[entity.id] = entity

    def get(self, entity_id: int):
        return self.books.get(entity_id)

    def get_all(self):
        return list(self.books.values())

    def delete(self, entity_id: int):
        if entity_id in self.books:
            del self.books[entity_id]


# -------------------- FACTORY --------------------

class BookFactory:
    """Создаёт нужный вид издания."""

    @staticmethod
    def create(book_type: BookType, book_id: int, title: str, author: str):
        if book_type == BookType.PRINTED:
            return PrintedBook(book_id, title, author)
        if book_type == BookType.ELECTRONIC:
            return ElectronicBook(book_id, title, author)
        if book_type == BookType.MAGAZINE:
            return Magazine(book_id, title, author)
        raise ValueError("Неизвестный тип издания")


# -------------------- STRATEGY --------------------

class LoanStrategy:
    """Общий интерфейс стратегий срока выдачи."""

    def get_days(self):
        raise NotImplementedError


class StandardLoanStrategy(LoanStrategy):
    def get_days(self):
        return 14


class PreferentialLoanStrategy(LoanStrategy):
    def get_days(self):
        return 21


class TeacherLoanStrategy(LoanStrategy):
    def get_days(self):
        return 30


# -------------------- СЕРВИС --------------------

class LibraryService:
    """Основная бизнес-логика библиотеки."""

    def __init__(self, repository: Repository):
        self.repository = repository

    def issue_book(self, book_id: int, reader: str, strategy: LoanStrategy):
        book = self.repository.get(book_id)
        if book is None:
            raise ValueError("Книга не найдена")

        if book.status == BookStatus.LOANED:
            raise ValueError("Книга уже выдана другому читателю")

        if book.status == BookStatus.RESERVED and book.reader != reader:
            raise ValueError(f"Книга забронирована читателем: {book.reader}")

        book.status = BookStatus.LOANED
        book.reader = reader
        book.loan_days = strategy.get_days()
        return book.loan_days

    def return_book(self, book_id: int):
        book = self.repository.get(book_id)
        if book is None:
            raise ValueError("Книга не найдена")

        if book.status != BookStatus.LOANED:
            raise ValueError("Книга не была выдана")

        book.status = BookStatus.AVAILABLE
        book.reader = ""
        book.loan_days = 0

    def reserve_book(self, book_id: int, reader: str):
        book = self.repository.get(book_id)
        if book is None:
            raise ValueError("Книга не найдена")

        if book.status != BookStatus.AVAILABLE:
            raise ValueError("Книгу нельзя забронировать (она выдана или уже забронирована)")

        book.status = BookStatus.RESERVED
        book.reader = reader


# -------------------- COMMAND --------------------

class Command(Protocol):
    def execute(self):
        ...


class IssueCommand:
    def __init__(self, service: LibraryService, book_id: int, reader: str,
                 strategy: LoanStrategy):
        self.service = service
        self.book_id = book_id
        self.reader = reader
        self.strategy = strategy

    def execute(self):
        return self.service.issue_book(self.book_id, self.reader, self.strategy)


class ReturnCommand:
    def __init__(self, service: LibraryService, book_id: int):
        self.service = service
        self.book_id = book_id

    def execute(self):
        self.service.return_book(self.book_id)


class ReserveCommand:
    def __init__(self, service: LibraryService, book_id: int, reader: str):
        self.service = service
        self.book_id = book_id
        self.reader = reader

    def execute(self):
        self.service.reserve_book(self.book_id, self.reader)


# -------------------- ДЕМОНСТРАЦИЯ --------------------

def print_books(repository):
    books = repository.get_all()
    if not books:
        print("Библиотека пуста.")
        return

    for book in books:
        extra = ""
        if book.reader:
            extra = f", читатель: {book.reader}"
        if book.loan_days:
            extra += f", срок: {book.loan_days} дн."

        print(
            f"{book.id}. {book.title} — {book.author}; "
            f"статус: {book.status.value}{extra}"
        )


def choose_strategy():
    print("1 - стандартный срок (14 дней)")
    print("2 - льготный срок (21 день)")
    print("3 - срок для преподавателей (30 дней)")
    choice = input("Выберите стратегию: ")

    if choice == "1":
        return StandardLoanStrategy()
    if choice == "2":
        return PreferentialLoanStrategy()
    if choice == "3":
        return TeacherLoanStrategy()

    raise ValueError("Неверный выбор стратегии")


def get_int_input(prompt: str) -> int:
    val = input(prompt).strip()
    if not val.isdigit():
        raise ValueError("ID должен быть целым числом")
    return int(val)


def add_book(repository):
    book_id = get_int_input("Введите ID издания: ")
    
    if repository.get(book_id) is not None:
        raise ValueError("Издание с таким ID уже существует")

    title = input("Введите название: ").strip()
    author = input("Введите автора: ").strip()

    if not title or not author:
        raise ValueError("Название и автор не могут быть пустыми")

    print("1 - печатная книга")
    print("2 - электронная книга")
    print("3 - журнал")
    choice = input("Выберите тип: ")

    if choice not in ("1", "2", "3"):
        raise ValueError("Неверный тип издания")

    book_type = BookType(choice)
    book = BookFactory.create(book_type, book_id, title, author)
    repository.add(book)
    print("Издание добавлено.")


def main():
    repository = InMemoryRepository()
    service = LibraryService(repository)

    # Начальные данные для демонстрации программы.
    repository.add(BookFactory.create(
        BookType.PRINTED, 1, "Мастер и Маргарита", "М. Булгаков"
    ))
    repository.add(BookFactory.create(
        BookType.ELECTRONIC, 2, "Python для начинающих", "А. Автор"
    ))
    repository.add(BookFactory.create(
        BookType.MAGAZINE, 3, "Мир технологий", "Редакция журнала"
    ))

    while True:
        print("\n===== БИБЛИОТЕКА =====")
        print("1 - показать издания")
        print("2 - добавить издание")
        print("3 - выдать издание")
        print("4 - вернуть издание")
        print("5 - забронировать издание")
        print("0 - выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                print_books(repository)

            elif choice == "2":
                add_book(repository)

            elif choice == "3":
                book_id = get_int_input("Введите ID издания: ")
                reader = input("Введите имя читателя: ").strip()
                if not reader:
                    raise ValueError("Имя читателя не может быть пустым")
                strategy = choose_strategy()
                command = IssueCommand(service, book_id, reader, strategy)
                days = command.execute()
                print(f"Издание выдано на {days} дней.")

            elif choice == "4":
                book_id = get_int_input("Введите ID издания: ")
                command = ReturnCommand(service, book_id)
                command.execute()
                print("Издание возвращено.")

            elif choice == "5":
                book_id = get_int_input("Введите ID издания: ")
                reader = input("Введите имя читателя: ").strip()
                if not reader:
                    raise ValueError("Имя читателя не может быть пустым")
                command = ReserveCommand(service, book_id, reader)
                command.execute()
                print("Издание забронировано.")

            elif choice == "0":
                print("Программа завершена.")
                break

            else:
                print("Ошибка: такого пункта меню нет.")

        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()