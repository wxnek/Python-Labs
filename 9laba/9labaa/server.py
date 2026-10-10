import json
import logging
import socket
import threading
import time

from exceptions import CalculationError, ProtocolError
from protocol import decode_message, encode_message, make_error, make_success
from repository import CalculationRepository
from service import Service

HOST = "127.0.0.1"
PORT = 5000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

repository = CalculationRepository()
service = Service(repository)


def calculation_to_dict(calculation):
    return {
        "id": calculation.id,
        "expression": calculation.expression,
        "result": calculation.result,
        "timestamp": calculation.timestamp,
    }


def handle_request(request: dict) -> dict:
    command = request["command"]
    data = request["data"]

    logging.info("Command: %s", command)

    if command == "list":
        calculations = [calculation_to_dict(item) for item in service.get_all()]
        return make_success(calculations)

    if command == "get":
        calculation_id = int(data["id"])
        return make_success(calculation_to_dict(service.get(calculation_id)))

    if command == "create":
        calculation = service.calculate(str(data["expression"]))
        return make_success(calculation_to_dict(calculation))

    if command == "update":
        calculation_id = int(data["id"])
        calculation = service.update(calculation_id, str(data["expression"]))
        return make_success(calculation_to_dict(calculation))

    if command == "delete":
        calculation_id = int(data["id"])
        service.delete(calculation_id)
        return make_success({"message": "Расчёт удалён"})

    # Специализированная команда варианта 2.
    if command == "calculate":
        calculation = service.calculate(str(data["expression"]))
        return make_success({
            "expression": calculation.expression,
            "result": calculation.result,
            "id": calculation.id,
        })

    # Команда для демонстрации тайм-аута клиента.
    if command == "slow":
        time.sleep(10)
        return make_success({"message": "Операция завершена"})

    return make_error("Неизвестная команда")


def handle_client(conn: socket.socket, address) -> None:
    logging.info("Client connected: %s:%s", address[0], address[1])
    conn.settimeout(5)
    buffer = ""

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue

                try:
                    request = decode_message(line)
                    response = handle_request(request)
                    conn.sendall(encode_message(response))
                    logging.info("Command completed: %s", request["command"])
                except (ProtocolError, CalculationError, KeyError, ValueError, TypeError) as error:
                    logging.error("Request error: %s", error)
                    conn.sendall(encode_message(make_error(str(error))))
                except BrokenPipeError:
                    logging.warning("Client closed connection before response")
                    return

    except socket.timeout:
        logging.warning("Client timeout: %s:%s", address[0], address[1])
    except (ConnectionResetError, OSError) as error:
        logging.warning("Connection error: %s", error)
    finally:
        conn.close()
        logging.info("Client disconnected: %s:%s", address[0], address[1])


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)

    logging.info("Server started on %s:%s", HOST, PORT)

    try:
        while True:
            try:
                conn, address = server.accept()
            except KeyboardInterrupt:
                break

            thread = threading.Thread(
                target=handle_client,
                args=(conn, address),
                daemon=True,
            )
            thread.start()
    finally:
        server.close()
        logging.info("Server stopped")


if __name__ == "__main__":
    main()
