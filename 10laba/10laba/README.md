# Лабораторная работа №10 — вариант 2

Предметная область: библиотека.
Основная сущность: `Book`.
Специализированная операция: поиск книг по автору.

## Структура

- `app.py` — Flask REST API.
- `models.py` — класс `Book`.
- `repository.py` — хранение книг в памяти.
- `service.py` — бизнес-логика.
- `exceptions.py` — пользовательские исключения.
- `client.py` — консольный HTTP-клиент.
- `tests/test_app.py` — автоматические тесты.

## Запуск

```bash
pip install -r requirements.txt
python app.py
```

В другом терминале:

```bash
python client.py
```

Тесты:

```bash
pytest -q
```

## Основные endpoints

- `GET /books`
- `GET /books/{id}`
- `POST /books`
- `PUT /books/{id}`
- `PATCH /books/{id}`
- `DELETE /books/{id}`
- `GET /books/search?q=...`
- `GET /books/by-author?author=...`
- `GET /books/statistics`

Для `/books` доступны фильтрация, сортировка и пагинация.
