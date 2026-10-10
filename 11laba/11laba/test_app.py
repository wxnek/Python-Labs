import pytest

from app import create_app
from database import get_connection, DB_PATH, init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    import database
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    monkeypatch.setattr(database, "SCHEMA_PATH", __import__("pathlib").Path(__file__).with_name("schema.sql"))
    init_db()
    connection = get_connection()
    connection.execute(
        "INSERT INTO readers(name, email) VALUES (?, ?)",
        ("Тестовый читатель", "test@example.com"),
    )
    connection.execute(
        """
        INSERT INTO books(title, author, year, isbn, category)
        VALUES (?, ?, ?, ?, ?)
        """,
        ("Тестовая книга", "Автор", 2020, "test-isbn", "Тест"),
    )
    connection.commit()
    connection.close()

    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_get_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_issue_and_return(client):
    issue_response = client.post("/loans", json={"reader_id": 1, "book_id": 1})
    assert issue_response.status_code == 201

    loan_id = issue_response.get_json()["id"]
    return_response = client.put(f"/loans/{loan_id}/return")
    assert return_response.status_code == 200


def test_cannot_issue_same_book_twice(client):
    first = client.post("/loans", json={"reader_id": 1, "book_id": 1})
    second = client.post("/loans", json={"reader_id": 1, "book_id": 1})
    assert first.status_code == 201
    assert second.status_code == 400
