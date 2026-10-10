from typing import Any

from flask import Flask, jsonify, request, send_from_directory

from database import get_connection, init_db
from redis_cache import RedisCache
from repository import LibraryRepository
from service import LibraryError, LibraryService


class InputError(Exception):
    pass



def create_app() -> Flask:
    init_db()

    app = Flask(__name__)
    app.json.ensure_ascii = False

    cache = RedisCache()

    @app.errorhandler(InputError)
    def input_error(error: InputError):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(LibraryError)
    def library_error(error: LibraryError):
        return jsonify({"error": str(error)}), 400


    @app.errorhandler(InputError)
    def input_error(error: InputError):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(LibraryError)
    def library_error(error: LibraryError):
        return jsonify({"error": str(error)}), 400

    @app.get("/books")
    def books():
        connection = get_connection()
        try:
            repository = LibraryRepository(connection)
            search = request.args.get("search")
            category = request.args.get("category")
            year_from = request.args.get("year_from", type=int)
            order = request.args.get("order", "asc")

            if search:
                result = repository.search_books(search)
            elif category or year_from is not None:
                result = repository.filter_books(category, year_from)
            else:
                result = repository.get_books()

            if order in ("asc", "desc") and not (category or year_from is not None):
                result = repository.sort_books(order == "desc")

            return jsonify(result)
        finally:
            connection.close()

    @app.get("/books/<int:book_id>")
    def book(book_id: int):
        cached = cache.get_book(book_id)
        if cached:
            cache.increase_views()
            cached["source"] = "Redis"
            return jsonify(cached)

        connection = get_connection()
        try:
            result = LibraryRepository(connection).get_book(book_id)
            if result is None:
                raise LibraryError("Книга не найдена")
            cache.set_book(result)
            cache.increase_views()
            result["source"] = "SQLite"
            return jsonify(result)
        finally:
            connection.close()

    @app.post("/books")
    def add_book():
        data: dict[str, Any] = request.get_json(silent=True) or {}
        required = ["title", "author", "year", "isbn", "category"]
        if any(field not in data for field in required):
            raise InputError("Нужно передать title, author, year, isbn и category")

        connection = get_connection()
        try:
            repository = LibraryRepository(connection)
            try:
                book_id = repository.add_book(
                    str(data["title"]),
                    str(data["author"]),
                    int(data["year"]),
                    str(data["isbn"]),
                    str(data["category"]),
                )
                connection.commit()
            except Exception as exc:
                connection.rollback()
                raise LibraryError("Не удалось добавить книгу. ISBN может быть занят.") from exc
            return jsonify({"id": book_id}), 201
        finally:
            connection.close()

    @app.put("/books/<int:book_id>")
    def update_book(book_id: int):
        data: dict[str, Any] = request.get_json(silent=True) or {}
        if "title" not in data or "category" not in data:
            raise InputError("Нужно передать title и category")

        connection = get_connection()
        try:
            repository = LibraryRepository(connection)
            changed = repository.update_book(book_id, str(data["title"]), str(data["category"]))
            if not changed:
                raise LibraryError("Книга не найдена")
            connection.commit()
            cache.delete_book(book_id)
            return jsonify(repository.get_book(book_id))
        finally:
            connection.close()

    @app.delete("/books/<int:book_id>")
    def delete_book(book_id: int):
        connection = get_connection()
        try:
            repository = LibraryRepository(connection)
            if repository.active_loan_for_book(book_id):
                raise LibraryError("Нельзя удалить выданную книгу")
            changed = repository.delete_book(book_id)
            if not changed:
                raise LibraryError("Книга не найдена")
            connection.commit()
            cache.delete_book(book_id)
            return jsonify({"message": "Книга удалена"})
        finally:
            connection.close()

    @app.get("/readers")
    def readers():
        connection = get_connection()
        try:
            return jsonify(LibraryRepository(connection).get_readers())
        finally:
            connection.close()

    @app.get("/loans")
    def loans():
        connection = get_connection()
        try:
            return jsonify(LibraryRepository(connection).get_loans())
        finally:
            connection.close()

    @app.post("/loans")
    def issue():
        data = request.get_json(silent=True) or {}
        try:
            reader_id = int(data["reader_id"])
            book_id = int(data["book_id"])
        except (KeyError, TypeError, ValueError) as exc:
            raise InputError("Нужно передать reader_id и book_id") from exc

        connection = get_connection()
        try:
            repository = LibraryRepository(connection)
            result = LibraryService(repository).issue_book(reader_id, book_id)
            cache.delete_book(book_id)
            return jsonify(result), 201
        finally:
            connection.close()

    @app.put("/loans/<int:loan_id>/return")
    def return_book(loan_id: int):
        connection = get_connection()
        try:
            repository = LibraryRepository(connection)
            result = LibraryService(repository).return_book(loan_id)
            cache.delete_book(result["book_id"])
            return jsonify(result)
        finally:
            connection.close()

    @app.get("/redis/demo")
    def redis_demo():
        return jsonify(cache.demo_operations())

    @app.get("/cdn/<path:filename>")
    def cdn(filename: str):
        response = send_from_directory("static", filename)
        response.headers["Cache-Control"] = "public, max-age=3600"
        return response

    @app.get("/")
    def index():
        return jsonify({
            "message": "Библиотека — ЛР №11, вариант 2",
            "endpoints": [
                "GET /books",
                "GET /books/<id>",
                "POST /books",
                "PUT /books/<id>",
                "DELETE /books/<id>",
                "GET /readers",
                "GET /loans",
                "POST /loans",
                "PUT /loans/<id>/return",
                "GET /redis/demo",
                "GET /cdn/<filename>",
            ],
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
