import threading
import time

class Queue:
    def __init__(self):
        """Инициализация очереди и рекурсивного блокировщика."""
        self.queue = []
        self.lock = threading.RLock()

    def enqueue(self, item):
        """Добавляет элемент в очередь."""
        with self.lock:
            self.queue.append(item)
            print(f"[{threading.current_thread().name}] Добавлено: {item}")

    def dequeue(self):
        """Удаляет элемент из очереди и возвращает его."""
        with self.lock:
            if not self.queue:
                print(f"[{threading.current_thread().name}] Очередь пуста")
                return None
            item = self.queue.pop(0)
            print(f"[{threading.current_thread().name}] Удалено: {item}")
            return item

    def is_empty(self):
        """Проверяет, пуста ли очередь."""
        with self.lock:
            return len(self.queue) == 0

def producer(queue, items):
    """Производитель: добавляет элементы в очередь."""
    for item in items:
        queue.enqueue(item)
        time.sleep(0.5)

def consumer(queue):
    """Потребитель: извлекает элементы из очереди."""
    while True:
        item = queue.dequeue()
        if item is None:
            break
        time.sleep(1)

if __name__ == "__main__":
    queue = Queue()

    items_to_add = [1, 2, 3, 4, 5]

    producer_thread = threading.Thread(target=producer, args=(queue, items_to_add), name="Producer")
    consumer_thread = threading.Thread(target=consumer, args=(queue,), name="Consumer")

    producer_thread.start()
    time.sleep(1)
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    print("Работа программы завершена.")
