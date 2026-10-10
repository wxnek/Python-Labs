from typing import List

from exceptions import BookNotFoundError
from models import Book


class BookRepository:
    def __init__(self) -> None:
        self.books: List[Book] = [
            Book(1, "Война и мир", "Лев Толстой", 1869, True),
            Book(2, "Мастер и Маргарита", "Михаил Булгаков", 1967, False),
        ]
        self.next_id: int = 3

    def add(self, title: str, author: str, year: int, available: bool) -> Book:
        book = Book(self.next_id, title, author, year, available)
        self.books.append(book)
        self.next_id += 1
        return book

    def get(self, book_id: int) -> Book:
        for book in self.books:
            if book.id == book_id:
                return book
        raise BookNotFoundError("Книга не найдена")

    def get_all(self) -> List[Book]:
        return self.books.copy()

    def update(self, book: Book) -> Book:
        for index, old_book in enumerate(self.books):
            if old_book.id == book.id:
                self.books[index] = book
                return book
        raise BookNotFoundError("Книга не найдена")

    def delete(self, book_id: int) -> None:
        book = self.get(book_id)
        self.books.remove(book)
