import threading
import time

def set_event(event, stop_event):
    """
    Устанавливает состояние объекта Event каждую секунду.
    """
    while not stop_event.is_set():  # Завершаем, если флаг остановки установлен
        time.sleep(1)
        event.set()  # Устанавливаем событие
        print("Состояние события установлено.")
        time.sleep(1)
        event.clear()  # Сбрасываем событие
        print("Состояние события сброшено.")
    print("SetterThread завершил работу.")

def wait_for_event(event, stop_event):
    """
    Ожидает наступления события и выводит сообщение, когда событие происходит.
    """
    while not stop_event.is_set():  # Завершаем, если флаг остановки установлен
        event.wait()  # Ожидание события
        if stop_event.is_set():  # Проверяем перед выводом, чтобы завершиться
            break
        print("Event occurred")
    print("WaiterThread завершил работу.")

def event_did_not_occur(event, stop_event):
    """
    Выводит сообщение, пока событие не наступило, затем завершает работу.
    """
    while not stop_event.is_set():  # Завершаем, если флаг остановки установлен
        if not event.is_set():  # Если событие не произошло
            print("Event did not occur")
            time.sleep(1)
        else:
            print("Событие произошло, третий поток завершает работу.")
            stop_event.set()  # Устанавливаем флаг остановки
            break
    print("NotOccurredThread завершил работу.")

def main():
    event = threading.Event()  # Основное событие
    stop_event = threading.Event()  # Флаг для остановки всех потоков

    # Создаем потоки
    thread_set = threading.Thread(target=set_event, args=(event, stop_event), name="SetterThread")
    thread_wait = threading.Thread(target=wait_for_event, args=(event, stop_event), name="WaiterThread")
    thread_not_occur = threading.Thread(target=event_did_not_occur, args=(event, stop_event), name="NotOccurredThread")

    # Запускаем потоки
    thread_set.start()
    thread_wait.start()
    thread_not_occur.start()

    # Ожидаем завершения всех потоков
    thread_not_occur.join()  # Ждем завершения третьего потока
    stop_event.set()  # Устанавливаем флаг завершения для остальных потоков

    thread_set.join()
    thread_wait.join()

    print("Все потоки завершены. Программа завершена.")

if __name__ == "__main__":
    main()
