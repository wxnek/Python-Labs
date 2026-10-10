# Лабораторная работа №11, вариант 2 — Библиотека

Использованы три таблицы: `readers`, `books`, `loans`.
Основная БД — SQLite. ORM не используется: SQL-запросы написаны вручную.

## Установка

```bash
python -m venv .venv
.venv\\Scripts\\activate      # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

## Запуск

1. Запустить Redis (для части NoSQL):

```bash
docker compose up -d
```

2. Заполнить БД:

```bash
python seed.py
```

3. Запустить REST API:

```bash
python app.py
```

После запуска:

- `GET http://127.0.0.1:5000/books`
- `GET http://127.0.0.1:5000/books/1`
- `GET http://127.0.0.1:5000/readers`
- `GET http://127.0.0.1:5000/loans`
- `GET http://127.0.0.1:5000/redis/demo`
- `GET http://127.0.0.1:5000/cdn/book.svg`

## Выдача книги

POST `/loans`:

```json
{
  "reader_id": 1,
  "book_id": 2
}
```

## Возврат

PUT `/loans/1/return`

## Тесты

```bash
pytest
```

## SQL

`queries.sql` содержит 15 обязательных примеров запросов.

## CDN

Внешний CDN в основной код не подключён, поэтому используется разрешённая методичкой локальная имитация CDN. Статические файлы лежат в `static/`, а маршрут `/cdn/...` добавляет `Cache-Control: public, max-age=3600`.
