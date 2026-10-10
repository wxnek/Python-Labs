import sqlite3
from typing import Any

from repository import LibraryRepository


class LibraryError(Exception):
    """Ошибка бизнес-логики библиотеки."""


class LibraryService:
    def __init__(self, repository: LibraryRepository):
        self.repository = repository

    def issue_book(self, reader_id: int, book_id: int) -> dict[str, Any]:
        reader = self.repository.get_reader(reader_id)
        book = self.repository.get_book(book_id)

        if reader is None:
            raise LibraryError("Читатель не найден")
        if book is None:
            raise LibraryError("Книга не найдена")
        if book["available"] == 0:
            raise LibraryError("Книга уже выдана")

        try:
            loan_id = self.repository.create_loan(reader_id, book_id)
            self.repository.set_book_available(book_id, 0)
            self.repository.connection.commit()
        except sqlite3.IntegrityError as exc:
            self.repository.connection.rollback()
            raise LibraryError("Не удалось выдать книгу") from exc
        except Exception as exc:
            self.repository.connection.rollback()
            raise LibraryError("Ошибка транзакции") from exc

        return self.repository.get_loan(loan_id) or {}

    def return_book(self, loan_id: int) -> dict[str, Any]:
        loan = self.repository.get_loan(loan_id)
        if loan is None:
            raise LibraryError("Выдача не найдена")
        if loan["return_date"] is not None:
            raise LibraryError("Книга уже возвращена")

        try:
            changed = self.repository.return_loan(loan_id)
            self.repository.set_book_available(loan["book_id"], 1)
            if not changed:
                raise LibraryError("Не удалось вернуть книгу")
            self.repository.connection.commit()
        except LibraryError:
            self.repository.connection.rollback()
            raise
        except Exception as exc:
            self.repository.connection.rollback()
            raise LibraryError("Ошибка транзакции") from exc

        return self.repository.get_loan(loan_id) or {}
