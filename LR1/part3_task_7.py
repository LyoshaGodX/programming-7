import threading
import time

def server(barrier):
    """Серверный поток: готовится к обработке запросов клиента."""
    print("[Сервер] Запуск рыбовприемника...")
    time.sleep(2)
    print("[Сервер] Рыбовприемник готов!")
    barrier.wait()
    print("[Сервер] Ожидаю рыбов...")

def client(barrier):
    """Клиентский поток: ожидает готовности сервера и отправляет запрос."""
    print("[Клиент] Ожидаю готовности рыбовприемника...")
    barrier.wait()
    print("[Клиент] Отправляю рыбов серверу...")
    time.sleep(1)
    print("[Клиент] Рыбовы успешно съедены!")

if __name__ == "__main__":
    barrier = threading.Barrier(2)

    server_thread = threading.Thread(target=server, args=(barrier,), name="Server")
    client_thread = threading.Thread(target=client, args=(barrier,), name="Client")

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()

    print("Клоунада завершена.")
