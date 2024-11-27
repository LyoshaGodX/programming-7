import math
import concurrent.futures as ftres
from functools import partial
import timeit
import threading
import os
import requests

def integrate(f, a, b, *, n_iter=1000):
    """
    Простое численное интегрирование методом прямоугольников.
    
    Parameters:
        f (function): Интегрируемая функция.
        a (float): Нижний предел интегрирования.
        b (float): Верхний предел интегрирования.
        n_iter (int): Количество итераций (разбиение на маленькие интервалы).
        
    Returns:
        float: Значение интеграла функции f на интервале [a, b].
    """
    step = (b - a) / n_iter
    result = 0.0
    for i in range(n_iter):
        x = a + i * step
        result += f(x) * step
    return result


def integrate_async(f, a, b, *, n_jobs=2, n_iter=1000):
    """
    Асинхронное интегрирование с использованием многопоточности или многозадачности.
    
    Parameters:
        f (function): Интегрируемая функция.
        a (float): Нижний предел интегрирования.
        b (float): Верхний предел интегрирования.
        n_jobs (int): Количество потоков или процессов.
        n_iter (int): Количество итераций.
        
    Returns:
        float: Результат асинхронного интегрирования.
    """
    step = (b - a) / n_jobs
    with ftres.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        spawn = partial(integrate, f, n_iter=n_iter // n_jobs)
        fs = [
            executor.submit(spawn, a + i * step, a + (i + 1) * step)
            for i in range(n_jobs)
        ]
        results = [f.result() for f in ftres.as_completed(fs)]
    return sum(results)


n_iter = 10**6
a = 0
b = math.pi / 2
f = math.atan

def measure_time(n_jobs):
    """
    Функция для измерения времени вычисления интеграла с помощью многопоточности.
    
    Parameters:
        n_jobs (int): Количество потоков для выполнения.
    """
    start_time = timeit.default_timer()
    result = integrate_async(f, a, b, n_jobs=n_jobs, n_iter=n_iter)
    elapsed_time = timeit.default_timer() - start_time
    print(f"Время для {n_jobs} потоков/процессов: {elapsed_time * 1000:.6f} ms")
    return elapsed_time


class BankAccount:
    def __init__(self, initial_balance=0):
        """
        Инициализация банковского счета с начальным балансом.
        
        Parameters:
            initial_balance (float): Начальный баланс счета (по умолчанию 0).
        """
        self.balance = initial_balance
        self.lock = threading.Lock()

    def deposit(self, amount):
        """
        Метод для внесения денег на счет в отдельном потоке.
        
        Parameters:
            amount (float): Сумма для внесения.
        """
        def task():
            with self.lock:
                print(f"Вносим {amount} на счет. Текущий баланс: {self.balance}")
                self.balance += amount
                print(f"После внесения: {self.balance}")

        thread = threading.Thread(target=task)
        thread.start()
        return thread

    def withdraw(self, amount):
        """
        Метод для снятия денег со счета в отдельном потоке.
        
        Parameters:
            amount (float): Сумма для снятия.
        """
        def task():
            with self.lock:
                if self.balance >= amount:
                    print(f"Снимаем {amount} с счета. Текущий баланс: {self.balance}")
                    self.balance -= amount
                    print(f"После снятия: {self.balance}")
                else:
                    print(f"Недостаточно средств для снятия {amount}. Текущий баланс: {self.balance}")

        thread = threading.Thread(target=task)
        thread.start()
        return thread

    def get_balance(self):
        """
        Метод для получения текущего баланса счета.
        
        Returns:
            float: Текущий баланс счета.
        """
        with self.lock:
            return self.balance

    def display_balance(self):
        """Метод для отображения текущего баланса на экране."""
        print(f"Текущий баланс: {self.get_balance()}")


MAX_THREADS = 5
semaphore = threading.Semaphore(MAX_THREADS)

def download_image(url, file_name):
    """
    Загружает изображение с указанного URL и сохраняет его в текущую директорию.

    Parameters:
        url (str): URL изображения
        file_name (str): Имя файла для сохранения
    """
    with semaphore:
        print(f"Загрузка {file_name} с {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open(file_name, 'wb') as f:
                f.write(response.content)

            print(f"Завершена загрузка {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке {file_name}: {e}")

def download_images(image_sizes, output_dir="images"):
    """
    Загружает несколько изображений с разными размерами из API picsum.photos.

    Parameters:
        image_sizes (list): Список кортежей (ширина, высота) для каждого изображения
        output_dir (str): Директория для сохранения изображений (по умолчанию "images")
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Создаем пул потоков
    with ftres.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for i, (width, height) in enumerate(image_sizes):
            url = f"https://picsum.photos/{width}/{height}"
            file_name = os.path.join(output_dir, f"image_{width}x{height}_{i+1}.jpg")

            future = executor.submit(download_image, url, file_name)
            futures.append(future)

        for future in ftres.as_completed(futures):
            future.result()

if __name__ == "__main__":
    for n_jobs in [2, 4, 6]:
        measure_time(n_jobs)    
    print()
        
    account = BankAccount(initial_balance=1000)

    threads = []

    threads.append(account.withdraw(300))
    threads.append(account.deposit(250))
    threads.append(account.withdraw(140))

    for t in threads:
        t.join()
    print()
    
    image_sizes = [
        (400, 400),   
        (800, 600),  
        (1200, 800),
        (500, 500),
        (1000, 1000),
        (600, 400)
    ]
    
    download_images(image_sizes)
