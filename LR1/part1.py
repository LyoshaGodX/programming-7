import math
import timeit
from threading import Thread, Lock
from multiprocessing import Pool, cpu_count

# Функция численного интегрирования
def integrate(f, a, b, n_iter=1000):
    '''
    Вычисляет интеграл функции f(x) от a до b с использованием метода прямоугольников.
    
    Parameters:
        f (callable): Функция одной переменной, которую нужно интегрировать.
        a (float): Левая граница интегрирования.
        b (float): Правая граница интегрирования.
        n_iter (int, optional): Число разбиений интервала [a, b]. По умолчанию 1000.
    
    Returns:
        float: Значение определенного интеграла функции f(x) от a до b.
    '''
    step = (b - a) / n_iter
    result = 0.0
    for i in range(n_iter):
        x = a + i * step
        result += f(x) * step
    return result

# Многопоточная версия
def integrate_threaded(f, a, b, n_iter=1000, n_threads=4):
    '''
    Вычисляет интеграл функции f(x) от a до b с использованием многопоточности.
    
    Parameters:
        f (callable): функция одной переменной, которую нужно интегрировать.
        a (float): левая граница интегрирования.
        b (float): павая граница интегрирования.
        n_iter (int, optional): число разбиений интервала [a, b]. По умолчанию 1000.
        n_threads (int, optional): число потоков для выполнения интегрирования. По умолчанию 4.
    
    Returns:
        float: Значение определенного интеграла функции f(x) от a до b.

    '''
    step = (b - a) / n_iter
    results = [0.0] * n_threads
    lock = Lock()

    def worker(start_idx, end_idx, thread_idx):
        local_result = 0.0
        for i in range(start_idx, end_idx):
            x = a + i * step
            local_result += f(x) * step
        with lock:
            results[thread_idx] = local_result

    threads = []
    chunk_size = n_iter // n_threads
    for i in range(n_threads):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < n_threads - 1 else n_iter
        thread = Thread(target=worker, args=(start_idx, end_idx, i))
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return sum(results)

# Функция для одного процесса (используется в multiprocessing)
def worker(f, a, b, start_idx, end_idx, step):
    '''
    Вычисляет интеграл функции f(x) от a до b с использованием одного процесса.
    
    Parameters:
        f (callable): функция одной переменной, которую нужно интегрировать.
        a (float): левая граница интегрирования.
        b (float): правая граница интегрирования.
        start_idx (int): индекс начала интервала для вычисления интеграла.
        end_idx (int): индекс конца интервала для вычисления интеграла.
        step (float): шаг разбиения интервала.
    
    Returns:
        float: Значение определенного интеграла функции f(x) от a до b.
    '''
    local_result = 0.0
    for i in range(start_idx, end_idx):
        x = a + i * step
        local_result += f(x) * step
    return local_result

# Многопроцессорная версия
def integrate_multiprocessing(f, a, b, n_iter=1000, n_processes=None):
    '''
    Вычисляет интеграл функции f(x) от a до b с использованием многопроцессорности.
    
    Parameters:
        f (callable): функция одной переменной, которую нужно интегрировать.
        a (float): левая граница интегрирования.
        b (float): правая граница интегрирования.
        n_iter (int, optional): число разбиений интервала [a, b]. По умолчанию 1000.
        n_processes (int, optional): число процессов для выполнения интегрирования. По умолчанию равно числу ядер процессора.
    
    Returns:
        float: Значение определенного интеграла функции f(x) от a до b.
    '''
    if n_processes is None:
        n_processes = cpu_count()

    step = (b - a) / n_iter
    chunk_size = n_iter // n_processes
    ranges = [
        (f, a, b, i * chunk_size, (i + 1) * chunk_size if i < n_processes - 1 else n_iter, step)
        for i in range(n_processes)
    ]

    with Pool(processes=n_processes) as pool:
        results = pool.starmap(worker, ranges)

    return sum(results)


def benchmark():
    funcs = [math.sin, math.cos, math.tan]
    a, b = 0, math.pi
    n_iters = [10**4, 10**5, 10**6, 10**8]

    for f in funcs:
        print(f"### Функция: {f.__name__}")
        for n_iter in n_iters:
            # Последовательное выполнение
            time_seq = timeit.timeit(lambda: integrate(f, a, b, n_iter), number=1)

            # Многопоточное выполнение
            time_thread = timeit.timeit(lambda: integrate_threaded(f, a, b, n_iter), number=1)

            # Многопроцессорное выполнение
            time_proc = timeit.timeit(lambda: integrate_multiprocessing(f, a, b, n_iter), number=1)

            thread_diff = time_seq - time_thread
            proc_diff = time_seq - time_proc

            print(f"n_iter={n_iter}:")
            print(f"  - Многопоточное решение {'быстрее' if thread_diff > 0 else 'медленнее'} на {abs(thread_diff) * 1000:.2f} ms в сравнении с последовательным")
            print(f"  - Многопроцессорное решение {'быстрее' if proc_diff > 0 else 'медленнее'} на {abs(proc_diff) * 1000:.2f} ms в сравнении с последовательным")
            print()

if __name__ == "__main__":
    benchmark()
