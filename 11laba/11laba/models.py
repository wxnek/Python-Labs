from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    year: int
    isbn: str
    category: str
    available: int = 1


@dataclass
class Reader:
    name: str
    email: str


@dataclass
class Loan:
    reader_id: int
    book_id: int
