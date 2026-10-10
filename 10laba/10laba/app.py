from flask import Flask, jsonify, request

from exceptions import BookNotFoundError, ValidationError
from repository import BookRepository
from service import BookService


def create_app(repository=None):
    app = Flask(__name__)
    service = BookService(repository or BookRepository())

    def get_data():
        data = request.get_json(silent=True)
        if data is None:
            raise ValidationError("Нужно передать JSON")
        if not isinstance(data, dict):
            raise ValidationError("JSON должен быть объектом")
        return data

    def get_int(name, default=None):
        value = request.args.get(name)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError as error:
            raise ValidationError(f"Параметр {name} должен быть целым числом") from error

    def get_bool(name):
        value = request.args.get(name)
        if value is None:
            return None
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        raise ValidationError(f"Параметр {name} должен быть true или false")

    @app.get("/books")
    def get_books():
        result = service.list_books(
            author=request.args.get("author"),
            available=get_bool("available"),
            year_from=get_int("year_from"),
            year_to=get_int("year_to"),
            sort=request.args.get("sort", "id"),
            order=request.args.get("order", "asc"),
            page=get_int("page", 1),
            limit=get_int("limit", 10),
        )
        return jsonify(result), 200

    @app.get("/books/search")
    def search_books():
        return jsonify(service.search(request.args.get("q"))), 200

    @app.get("/books/by-author")
    def search_by_author():
        return jsonify(service.search_by_author(request.args.get("author"))), 200

    @app.get("/books/statistics")
    def statistics():
        return jsonify(service.statistics()), 200

    @app.get("/books/<int:book_id>")
    def get_book(book_id):
        return jsonify(service.get(book_id).to_dict()), 200

    @app.post("/books")
    def create_book():
        book = service.create(get_data())
        return jsonify(book.to_dict()), 201

    @app.put("/books/<int:book_id>")
    def update_book(book_id):
        book = service.update(book_id, get_data())
        return jsonify(book.to_dict()), 200

    @app.patch("/books/<int:book_id>")
    def patch_book(book_id):
        book = service.patch(book_id, get_data())
        return jsonify(book.to_dict()), 200

    @app.delete("/books/<int:book_id>")
    def delete_book(book_id):
        service.delete(book_id)
        return "", 204

    @app.errorhandler(BookNotFoundError)
    def handle_not_found(error):
        return jsonify({"error": str(error), "code": "BOOK_NOT_FOUND"}), 404

    @app.errorhandler(ValidationError)
    def handle_validation(error):
        return jsonify({"error": str(error), "code": "BAD_REQUEST"}), 400

    @app.errorhandler(404)
    def handle_route_not_found(error):
        return jsonify({"error": "Маршрут не найден", "code": "NOT_FOUND"}), 404

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
