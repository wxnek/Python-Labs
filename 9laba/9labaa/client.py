import socket

from protocol import encode_message, decode_response

HOST = "127.0.0.1"
PORT = 5000
TIMEOUT = 5


def request(sock: socket.socket, command: str, data: dict) -> dict:
    message = {"command": command, "data": data}
    sock.sendall(encode_message(message))

    buffer = ""
    while "\n" not in buffer:
        part = sock.recv(4096)
        if not part:
            raise ConnectionError("Сервер закрыл соединение")
        buffer += part.decode("utf-8")

    line = buffer.split("\n", 1)[0]
    return decode_response(line)


def print_response(response: dict) -> None:
    print("\nОтвет сервера:")
    print(response)


def timeout_test() -> None:
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.settimeout(TIMEOUT)

    try:
        test_socket.connect((HOST, PORT))
        test_socket.sendall(encode_message({"command": "slow", "data": {}}))
        test_socket.recv(4096)
    except socket.timeout:
        print("Тайм-аут сработал: сервер отвечал дольше 5 секунд.")
    finally:
        test_socket.close()


def main() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)

    try:
        sock.connect((HOST, PORT))
        print("Подключение к серверу выполнено.")
    except OSError as error:
        print(f"Не удалось подключиться к серверу: {error}")
        sock.close()
        return

    try:
        while True:
            print("\n=== CLIENT ===")
            print("1. Получить список")
            print("2. Получить расчёт")
            print("3. Создать расчёт")
            print("4. Изменить расчёт")
            print("5. Удалить расчёт")
            print("6. Вычислить выражение")
            print("7. Проверить тайм-аут")
            print("0. Выход")

            choice = input("Введите команду: ")

            try:
                if choice == "1":
                    response = request(sock, "list", {})
                    print_response(response)

                elif choice == "2":
                    calculation_id = int(input("ID расчёта: "))
                    response = request(sock, "get", {"id": calculation_id})
                    print_response(response)

                elif choice == "3":
                    expression = input("Выражение: ")
                    response = request(sock, "create", {"expression": expression})
                    print_response(response)

                elif choice == "4":
                    calculation_id = int(input("ID расчёта: "))
                    expression = input("Новое выражение: ")
                    response = request(
                        sock,
                        "update",
                        {"id": calculation_id, "expression": expression},
                    )
                    print_response(response)

                elif choice == "5":
                    calculation_id = int(input("ID расчёта: "))
                    response = request(sock, "delete", {"id": calculation_id})
                    print_response(response)

                elif choice == "6":
                    expression = input("Выражение: ")
                    response = request(sock, "calculate", {"expression": expression})
                    print_response(response)

                elif choice == "7":
                    timeout_test()

                elif choice == "0":
                    break

                else:
                    print("Неизвестный пункт меню.")

            except (ValueError, ConnectionError, socket.timeout, OSError) as error:
                print(f"Ошибка: {error}")

    finally:
        sock.close()
        print("Клиент завершён.")


if __name__ == "__main__":
    main()
