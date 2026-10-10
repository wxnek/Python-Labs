import json

from exceptions import ProtocolError


def encode_message(message: dict) -> bytes:
    return (json.dumps(message, ensure_ascii=False) + "\n").encode("utf-8")


def decode_message(line: str) -> dict:
    try:
        message = json.loads(line)
    except json.JSONDecodeError as error:
        raise ProtocolError("Некорректный JSON") from error

    if not isinstance(message, dict):
        raise ProtocolError("Запрос должен быть JSON-объектом")

    if "command" not in message:
        raise ProtocolError("Отсутствует поле command")

    if "data" not in message:
        raise ProtocolError("Отсутствует поле data")

    if not isinstance(message["data"], dict):
        raise ProtocolError("Поле data должно быть объектом")

    return message


def make_success(data: object) -> dict:
    return {"status": "ok", "data": data}


def make_error(message: str) -> dict:
    return {"status": "error", "error": message}


def decode_response(line: str) -> dict:
    try:
        response = json.loads(line)
    except json.JSONDecodeError as error:
        raise ProtocolError("Некорректный JSON") from error

    if not isinstance(response, dict):
        raise ProtocolError("Ответ должен быть JSON-объектом")

    return response
