import pytest

from app import create_app
from repository import BookRepository
from service import BookService


@pytest.fixture
def repository():
    return BookRepository()


@pytest.fixture
def service(repository):
    return BookService(repository)


@pytest.fixture
def client(repository):
    app = create_app(repository)
    app.config["TESTING"] = True
    return app.test_client()


def test_repository_get(repository):
    assert repository.get(1).title == "Война и мир"


def test_repository_add(repository):
    book = repository.add("1984", "Джордж Оруэлл", 1949, True)
    assert book.id == 3
    assert repository.get(3).title == "1984"


def test_service_search_by_author(service):
    books = service.search_by_author("Толстой")
    assert len(books) == 1
    assert books[0]["title"] == "Война и мир"


def test_service_filter_and_sort(service):
    result = service.list_books(available=True, sort="year", order="asc")
    assert result["total"] == 1
    assert result["items"][0]["year"] == 1869


def test_service_statistics(service):
    result = service.statistics()
    assert result["total_books"] == 2
    assert result["available_books"] == 1


def test_api_get_list(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json["total"] == 2


def test_api_get_one(client):
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json["author"] == "Лев Толстой"


def test_api_create(client):
    response = client.post(
        "/books",
        json={
            "title": "1984",
            "author": "Джордж Оруэлл",
            "year": 1949,
            "available": True,
        },
    )
    assert response.status_code == 201
    assert response.json["id"] == 3


def test_api_put(client):
    response = client.put(
        "/books/1",
        json={
            "title": "Война и мир",
            "author": "Лев Толстой",
            "year": 1870,
            "available": True,
        },
    )
    assert response.status_code == 200
    assert response.json["year"] == 1870


def test_api_patch(client):
    response = client.patch("/books/2", json={"available": True})
    assert response.status_code == 200
    assert response.json["available"] is True


def test_api_not_found(client):
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json["code"] == "BOOK_NOT_FOUND"


def test_api_delete(client):
    response = client.delete("/books/1")
    assert response.status_code == 204


def test_api_by_author(client):
    response = client.get("/books/by-author?author=Булгаков")
    assert response.status_code == 200
    assert len(response.json) == 1


def test_api_validation(client):
    response = client.post(
        "/books",
        json={"title": "", "author": "Автор", "year": 2020, "available": True},
    )
    assert response.status_code == 400
