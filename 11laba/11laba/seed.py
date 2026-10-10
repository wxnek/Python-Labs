from database import get_connection, init_db


def seed() -> None:
    init_db()
    connection = get_connection()
    try:
        readers = [
            ("Иван Петров", "ivan@example.com"),
            ("Анна Сидорова", "anna@example.com"),
            ("Пётр Иванов", "petr@example.com"),
            ("Мария Смирнова", "maria@example.com"),
            ("Олег Кузнецов", "oleg@example.com"),
        ]

        books = [
            ("Мастер и Маргарита", "Михаил Булгаков", 1967, "9785171159999", "Роман"),
            ("Преступление и наказание", "Фёдор Достоевский", 1866, "9785170901101", "Роман"),
            ("1984", "Джордж Оруэлл", 1949, "9780451524935", "Антиутопия"),
            ("Три товарища", "Эрих Мария Ремарк", 1936, "9785699546732", "Роман"),
            ("Пикник на обочине", "Аркадий и Борис Стругацкие", 1972, "9785170874313", "Фантастика"),
            ("Дюна", "Фрэнк Герберт", 1965, "9780441172719", "Фантастика"),
            ("Гарри Поттер и философский камень", "Дж. К. Роулинг", 1997, "9780747532699", "Фэнтези"),
            ("Война и мир", "Лев Толстой", 1869, "9785171093218", "Роман"),
            ("451 градус по Фаренгейту", "Рэй Брэдбери", 1953, "9781451678182", "Антиутопия"),
            ("Солярис", "Станислав Лем", 1961, "9780451457998", "Фантастика"),
        ]

        connection.executemany(
            "INSERT OR IGNORE INTO readers(name, email) VALUES (?, ?)", readers
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO books(title, author, year, isbn, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            books,
        )

        connection.execute(
            """
            INSERT INTO loans(reader_id, book_id)
            SELECT 1, 1
            WHERE NOT EXISTS (
                SELECT 1 FROM loans WHERE reader_id = 1 AND book_id = 1 AND return_date IS NULL
            ) AND EXISTS (
                SELECT 1 FROM books WHERE id = 1 AND available = 1
            )
            """
        )
        connection.execute("UPDATE books SET available = 0 WHERE id = 1")

        connection.execute(
            """
            INSERT INTO loans(reader_id, book_id)
            SELECT 2, 3
            WHERE NOT EXISTS (
                SELECT 1 FROM loans WHERE reader_id = 2 AND book_id = 3 AND return_date IS NULL
            ) AND EXISTS (
                SELECT 1 FROM books WHERE id = 3 AND available = 1
            )
            """
        )
        connection.execute("UPDATE books SET available = 0 WHERE id = 3")

        connection.commit()
        print("База данных заполнена тестовыми данными.")
    finally:
        connection.close()


if __name__ == "__main__":
    seed()
