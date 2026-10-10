import requests

BASE_URL = "http://127.0.0.1:5000"


def show_response(response):
    print("Код:", response.status_code)
    if response.content:
        print(response.json())
    print()


def get_all():
    response = requests.get(f"{BASE_URL}/books")
    show_response(response)


def get_one():
    book_id = int(input("ID книги: "))
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    show_response(response)


def create_book():
    data = {
        "title": input("Название: "),
        "author": input("Автор: "),
        "year": int(input("Год: ")),
        "available": input("Доступна? (true/false): ").lower() == "true",
    }
    response = requests.post(f"{BASE_URL}/books", json=data)
    show_response(response)


def update_book():
    book_id = int(input("ID книги: "))
    data = {
        "title": input("Название: "),
        "author": input("Автор: "),
        "year": int(input("Год: ")),
        "available": input("Доступна? (true/false): ").lower() == "true",
    }
    response = requests.put(f"{BASE_URL}/books/{book_id}", json=data)
    show_response(response)


def patch_book():
    book_id = int(input("ID книги: "))
    field = input("Что изменить (title/author/year/available): ")
    value = input("Новое значение: ")

    if field == "year":
        value = int(value)
    elif field == "available":
        value = value.lower() == "true"

    response = requests.patch(
        f"{BASE_URL}/books/{book_id}",
        json={field: value},
    )
    show_response(response)


def delete_book():
    book_id = int(input("ID книги: "))
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    show_response(response)


def filter_books():
    params = {}
    author = input("Автор (Enter — без фильтра): ")
    available = input("Доступна? true/false/Enter: ").lower()

    if author:
        params["author"] = author
    if available in ("true", "false"):
        params["available"] = available

    response = requests.get(f"{BASE_URL}/books", params=params)
    show_response(response)


def sort_books():
    sort = input("Поле (title/year/author): ")
    order = input("Порядок (asc/desc): ")
    response = requests.get(
        f"{BASE_URL}/books",
        params={"sort": sort, "order": order},
    )
    show_response(response)


def by_author():
    author = input("Автор для поиска: ")
    response = requests.get(
        f"{BASE_URL}/books/by-author",
        params={"author": author},
    )
    show_response(response)


def main():
    while True:
        print("=========================")
        print("       REST CLIENT")
        print("=========================")
        print("1. Получить список")
        print("2. Получить объект")
        print("3. Создать")
        print("4. Изменить")
        print("5. Частично изменить")
        print("6. Удалить")
        print("7. Фильтрация")
        print("8. Сортировка")
        print("9. Поиск по автору")
        print("0. Выход")

        choice = input("Выберите действие: ")
        print()

        try:
            if choice == "1":
                get_all()
            elif choice == "2":
                get_one()
            elif choice == "3":
                create_book()
            elif choice == "4":
                update_book()
            elif choice == "5":
                patch_book()
            elif choice == "6":
                delete_book()
            elif choice == "7":
                filter_books()
            elif choice == "8":
                sort_books()
            elif choice == "9":
                by_author()
            elif choice == "0":
                break
            else:
                print("Неизвестный пункт меню.\n")
        except (ValueError, requests.RequestException) as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()
