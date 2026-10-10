import json
from typing import Any

try:
    import redis
except ImportError:
    redis = None


class RedisCache:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.client = None
        if redis is not None:
            try:
                self.client = redis.Redis(host=host, port=port, decode_responses=True)
                self.client.ping()
            except Exception:
                self.client = None

    def get_book(self, book_id: int) -> dict[str, Any] | None:
        if self.client is None:
            return None
        value = self.client.get(f"book:{book_id}")
        return json.loads(value) if value else None

    def set_book(self, book: dict[str, Any]) -> None:
        if self.client is None:
            return
        key = f"book:{book['id']}"
        self.client.set(key, json.dumps(book, ensure_ascii=False))
        self.client.expire(key, 60)

    def delete_book(self, book_id: int) -> None:
        if self.client is not None:
            self.client.delete(f"book:{book_id}")

    def increase_views(self) -> int:
        if self.client is None:
            return 0
        return int(self.client.incr("library:views"))

    def demo_operations(self) -> dict[str, Any]:
        if self.client is None:
            return {"redis": "недоступен"}
        self.client.set("library:test", "ok")
        value = self.client.get("library:test")
        self.client.expire("library:test", 30)
        counter = self.client.incr("library:test_counter")
        self.client.delete("library:test")
        return {"get": value, "counter": counter, "operations": "SET, GET, EXPIRE, INCR, DELETE"}
