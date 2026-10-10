from abc import ABC, abstractmethod
from enum import Enum
from typing import Protocol


# Статус книги
class BookStatus(Enum):
    AVAILABLE = "доступна"
    ISSUED = "выдана"


# Базовый класс книги
class Book(ABC):
    def __init__(self, book_id, title, author):
        self.id = book_id
        self.title = title
        self.author = author
        self.status = BookStatus.AVAILABLE
        self.reader_id = None
        self.reserved_by = None

    @abstractmethod
    def get_info(self):
        pass


# Печатная книга
class PrintedBook(Book):
    def __init__(self, book_id, title, author, pages):
        super().__init__(book_id, title, author)
        self.pages = pages

    def get_info(self):
        return (
            f"Печатная книга: {self.title}, "
            f"{self.author}, {self.pages} стр."
        )


# Электронная книга
class EBook(Book):
    def __init__(self, book_id, title, author, size_mb):
        super().__init__(book_id, title, author)
        self.size_mb = size_mb

    def get_info(self):
        return (
            f"Электронная книга: {self.title}, "
            f"{self.author}, {self.size_mb} МБ"
        )


# Читатель
class Reader:
    def __init__(self, reader_id, name, email, phone):
        self.id = reader_id
        self.name = name
        self.email = email
        self.phone = phone


# Интерфейс чтения данных
class LibraryReadRepository(Protocol):
    def get_book(self, book_id):
        ...

    def get_reader(self, reader_id):
        ...

    def get_all_books(self):
        ...


# Интерфейс изменения данных
class LibraryWriteRepository(Protocol):
    def add_book(self, book):
        ...

    def add_reader(self, reader):
        ...

    def save_book(self, book):
        ...


# Интерфейс отправки уведомлений
class NotificationSender(Protocol):
    def send(self, reader, message):
        ...


# Репозиторий, который хранит данные в памяти
class InMemoryRepository:
    def __init__(self):
        self.books = {}
        self.readers = {}

    def add_book(self, book):
        self.books[book.id] = book

    def add_reader(self, reader):
        self.readers[reader.id] = reader

    def save_book(self, book):
        self.books[book.id] = book

    def get_book(self, book_id):
        return self.books.get(book_id)

    def get_reader(self, reader_id):
        return self.readers.get(reader_id)

    def get_all_books(self):
        return list(self.books.values())


# Отправка по электронной почте
class EmailSender:
    def send(self, reader, message):
        print(f"EMAIL -> {reader.email}: {message}")


# Отправка по SMS
class SmsSender:
    def send(self, reader, message):
        print(f"SMS -> {reader.phone}: {message}")


# Основная логика библиотеки
class LibraryService:
    def __init__(self, book_reader, book_writer, notifier):
        self.book_reader = book_reader
        self.book_writer = book_writer
        self.notifier = notifier

    # Выдача книги
    def issue_book(self, book_id, reader_id):
        book = self.book_reader.get_book(book_id)
        reader = self.book_reader.get_reader(reader_id)

        if book is None or reader is None:
            print("Книга или читатель не найдены.")
            return

        if book.status != BookStatus.AVAILABLE:
            print("Книга недоступна.")
            return

        book.status = BookStatus.ISSUED
        book.reader_id = reader_id

        self.book_writer.save_book(book)

        self.notifier.send(
            reader,
            f"Книга '{book.title}' выдана вам."
        )

    # Возврат книги
    def return_book(self, book_id):
        book = self.book_reader.get_book(book_id)

        if book is None:
            print("Книга не найдена.")
            return

        reader = None

        if book.reader_id is not None:
            reader = self.book_reader.get_reader(book.reader_id)

        book.status = BookStatus.AVAILABLE
        book.reader_id = None

        self.book_writer.save_book(book)

        if reader is not None:
            self.notifier.send(
                reader,
                f"Книга '{book.title}' возвращена."
            )

    # Бронирование книги
    def reserve_book(self, book_id, reader_id):
        book = self.book_reader.get_book(book_id)
        reader = self.book_reader.get_reader(reader_id)

        if book is None or reader is None:
            print("Книга или читатель не найдены.")
            return

        if book.status == BookStatus.AVAILABLE:
            print("Свободную книгу бронировать не нужно.")
            return

        if book.reserved_by is not None:
            print("Книга уже забронирована.")
            return

        book.reserved_by = reader_id

        self.book_writer.save_book(book)

        self.notifier.send(
            reader,
            f"Книга '{book.title}' забронирована вами."
        )

    # Отдельное уведомление читателя
    def notify_reader(self, reader_id, message):
        reader = self.book_reader.get_reader(reader_id)

        if reader is not None:
            self.notifier.send(reader, message)

    # Получить все книги
    def get_books(self):
        return self.book_reader.get_all_books()


# Консольный интерфейс
class ConsoleUI:
    def __init__(self, service):
        self.service = service

    def show_books(self):
        print("\nСписок книг:")

        for book in self.service.get_books():
            print(
                f"{book.id}. "
                f"{book.get_info()} — {book.status.value}"
            )

    def run(self):
        while True:
            print("\n1 — Выдать книгу")
            print("2 — Вернуть книгу")
            print("3 — Забронировать книгу")
            print("4 — Показать книги")
            print("5 — Уведомить читателя")
            print("0 — Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                book_id = int(input("ID книги: "))
                reader_id = int(input("ID читателя: "))

                self.service.issue_book(book_id, reader_id)

            elif choice == "2":
                book_id = int(input("ID книги: "))

                self.service.return_book(book_id)

            elif choice == "3":
                book_id = int(input("ID книги: "))
                reader_id = int(input("ID читателя: "))

                self.service.reserve_book(book_id, reader_id)

            elif choice == "4":
                self.show_books()

            elif choice == "5":
                reader_id = int(input("ID читателя: "))
                message = input("Текст уведомления: ")

                self.service.notify_reader(
                    reader_id,
                    message
                )

            elif choice == "0":
                break

            else:
                print("Неизвестная команда.")


def main():
    # Создаём репозиторий
    repository = InMemoryRepository()

    # Добавляем книги
    repository.add_book(
        PrintedBook(
            1,
            "Преступление и наказание",
            "Ф. Достоевский",
            672
        )
    )

    repository.add_book(
        PrintedBook(
            2,
            "Мастер и Маргарита",
            "М. Булгаков",
            480
        )
    )

    repository.add_book(
        EBook(
            3,
            "1984",
            "Дж. Оруэлл",
            2.1
        )
    )

    # Добавляем читателей
    repository.add_reader(
        Reader(
            1,
            "Иван Петров",
            "ivan@mail.ru",
            "+79990001122"
        )
    )

    repository.add_reader(
        Reader(
            2,
            "Анна Смирнова",
            "anna@mail.ru",
            "+79990002233"
        )
    )

    # Выбор способа уведомления
    notification_type = input(
        "1 — Email, 2 — SMS: "
    )

    if notification_type == "2":
        notifier = SmsSender()
    else:
        notifier = EmailSender()

    # Внедрение зависимостей
    service = LibraryService(
        repository,
        repository,
        notifier
    )

    # Запуск интерфейса
    ui = ConsoleUI(service)
    ui.run()


if __name__ == "__main__":
    main()