import sqlite3
from typing import Any


class RepositoryError(Exception):
    """Ошибка работы с базой данных."""


class LibraryRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def get_books(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT * FROM books ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_book(self, book_id: int) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT * FROM books WHERE id = ?", (book_id,)
        ).fetchone()
        return dict(row) if row else None

    def search_books(self, text: str) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ?
            ORDER BY title
            """,
            (f"%{text}%", f"%{text}%"),
        ).fetchall()
        return [dict(row) for row in rows]

    def filter_books(self, category: str | None = None,
                     year_from: int | None = None) -> list[dict[str, Any]]:
        query = "SELECT * FROM books WHERE 1=1"
        params: list[Any] = []

        if category:
            query += " AND category = ?"
            params.append(category)
        if year_from is not None:
            query += " AND year >= ?"
            params.append(year_from)

        query += " ORDER BY year DESC"
        rows = self.connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def sort_books(self, reverse: bool = False) -> list[dict[str, Any]]:
        order = "DESC" if reverse else "ASC"
        rows = self.connection.execute(
            f"SELECT * FROM books ORDER BY year {order}"
        ).fetchall()
        return [dict(row) for row in rows]

    def add_book(self, title: str, author: str, year: int,
                 isbn: str, category: str) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO books(title, author, year, isbn, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, author, year, isbn, category),
        )
        return int(cursor.lastrowid)

    def update_book(self, book_id: int, title: str, category: str) -> bool:
        cursor = self.connection.execute(
            "UPDATE books SET title = ?, category = ? WHERE id = ?",
            (title, category, book_id),
        )
        return cursor.rowcount > 0

    def delete_book(self, book_id: int) -> bool:
        cursor = self.connection.execute(
            "DELETE FROM books WHERE id = ?", (book_id,)
        )
        return cursor.rowcount > 0

    def get_reader(self, reader_id: int) -> dict[str, Any] | None:
        row = self.connection.execute(
            "SELECT * FROM readers WHERE id = ?", (reader_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_readers(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            "SELECT * FROM readers ORDER BY name"
        ).fetchall()
        return [dict(row) for row in rows]

    def get_loan(self, loan_id: int) -> dict[str, Any] | None:
        row = self.connection.execute(
            """
            SELECT loans.id, loans.reader_id, readers.name AS reader_name,
                   loans.book_id, books.title, loans.loan_date, loans.return_date
            FROM loans
            JOIN readers ON readers.id = loans.reader_id
            JOIN books ON books.id = loans.book_id
            WHERE loans.id = ?
            """,
            (loan_id,),
        ).fetchone()
        return dict(row) if row else None

    def get_loans(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT loans.id, readers.name AS reader_name,
                   books.title, loans.loan_date, loans.return_date
            FROM loans
            JOIN readers ON readers.id = loans.reader_id
            JOIN books ON books.id = loans.book_id
            ORDER BY loans.id
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def active_loan_for_book(self, book_id: int) -> dict[str, Any] | None:
        row = self.connection.execute(
            """
            SELECT * FROM loans
            WHERE book_id = ? AND return_date IS NULL
            """,
            (book_id,),
        ).fetchone()
        return dict(row) if row else None

    def create_loan(self, reader_id: int, book_id: int) -> int:
        cursor = self.connection.execute(
            "INSERT INTO loans(reader_id, book_id) VALUES (?, ?)",
            (reader_id, book_id),
        )
        return int(cursor.lastrowid)

    def return_loan(self, loan_id: int) -> bool:
        cursor = self.connection.execute(
            """
            UPDATE loans
            SET return_date = CURRENT_DATE
            WHERE id = ? AND return_date IS NULL
            """,
            (loan_id,),
        )
        return cursor.rowcount > 0

    def set_book_available(self, book_id: int, available: int) -> None:
        self.connection.execute(
            "UPDATE books SET available = ? WHERE id = ?",
            (available, book_id),
        )
