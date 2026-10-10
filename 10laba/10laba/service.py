from typing import Any, Dict, Optional

from exceptions import ValidationError


class BookService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def _validate(self, data: Dict[str, Any], partial: bool = False) -> None:
        required = ["title", "author", "year", "available"]

        if not partial:
            for field in required:
                if field not in data:
                    raise ValidationError(f"Поле '{field}' обязательно")

        if "title" in data and (not isinstance(data["title"], str) or not data["title"].strip()):
            raise ValidationError("Название книги не должно быть пустым")

        if "author" in data and (not isinstance(data["author"], str) or not data["author"].strip()):
            raise ValidationError("Автор не должен быть пустым")

        if "year" in data and (not isinstance(data["year"], int) or data["year"] < 0):
            raise ValidationError("Год должен быть неотрицательным целым числом")

        if "available" in data and not isinstance(data["available"], bool):
            raise ValidationError("Поле available должно быть true или false")

    def create(self, data: Dict[str, Any]):
        self._validate(data)
        return self.repository.add(
            data["title"].strip(),
            data["author"].strip(),
            data["year"],
            data["available"],
        )

    def get(self, book_id: int):
        return self.repository.get(book_id)

    def update(self, book_id: int, data: Dict[str, Any]):
        self._validate(data)
        book = self.repository.get(book_id)
        book.title = data["title"].strip()
        book.author = data["author"].strip()
        book.year = data["year"]
        book.available = data["available"]
        return self.repository.update(book)

    def patch(self, book_id: int, data: Dict[str, Any]):
        if not data:
            raise ValidationError("Тело запроса не должно быть пустым")

        self._validate(data, partial=True)
        book = self.repository.get(book_id)

        if "title" in data:
            book.title = data["title"].strip()
        if "author" in data:
            book.author = data["author"].strip()
        if "year" in data:
            book.year = data["year"]
        if "available" in data:
            book.available = data["available"]

        return self.repository.update(book)

    def delete(self, book_id: int) -> None:
        self.repository.delete(book_id)

    def list_books(
        self,
        author: Optional[str] = None,
        available: Optional[bool] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sort: str = "id",
        order: str = "asc",
        page: int = 1,
        limit: int = 10,
    ) -> Dict[str, Any]:
        if page < 1 or limit < 1:
            raise ValidationError("page и limit должны быть больше нуля")

        books = self.repository.get_all()

        if author:
            books = [book for book in books if author.lower() in book.author.lower()]

        if available is not None:
            books = [book for book in books if book.available == available]

        if year_from is not None:
            books = [book for book in books if book.year >= year_from]

        if year_to is not None:
            books = [book for book in books if book.year <= year_to]

        sort_fields = {
            "id": lambda book: book.id,
            "title": lambda book: book.title.lower(),
            "author": lambda book: book.author.lower(),
            "year": lambda book: book.year,
        }

        if sort not in sort_fields:
            raise ValidationError("Сортировка доступна по id, title, author или year")

        if order not in ("asc", "desc"):
            raise ValidationError("order должен быть asc или desc")

        books.sort(key=sort_fields[sort], reverse=(order == "desc"))

        total = len(books)
        start = (page - 1) * limit
        end = start + limit

        return {
            "items": [book.to_dict() for book in books[start:end]],
            "page": page,
            "limit": limit,
            "total": total,
        }

    def search(self, query: Optional[str]):
        if not query:
            raise ValidationError("Параметр q обязателен")

        query = query.lower()
        books = [
            book
            for book in self.repository.get_all()
            if query in book.title.lower() or query in book.author.lower()
        ]
        return [book.to_dict() for book in books]

    def search_by_author(self, author: Optional[str]):
        if not author:
            raise ValidationError("Параметр author обязателен")

        author = author.lower()
        books = [
            book
            for book in self.repository.get_all()
            if author in book.author.lower()
        ]
        return [book.to_dict() for book in books]

    def statistics(self) -> Dict[str, Any]:
        books = self.repository.get_all()
        years = [book.year for book in books]
        available = sum(book.available for book in books)

        return {
            "total_books": len(books),
            "available_books": available,
            "unavailable_books": len(books) - available,
            "oldest_year": min(years) if years else None,
            "newest_year": max(years) if years else None,
        }
