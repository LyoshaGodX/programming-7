import threading
import requests
import math


def download_file(url, thread_name):
    '''
    Загружает файл по указанному URL и сохраняет его в текущую директорию.
    
    Parameters:
        url (str): URL файла
        thread_name (str): Имя потока
    '''
    print(f"Поток {thread_name} начал скачивание файла с {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        file_name = url.split("/")[-1]
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Поток {thread_name} завершил скачивание файла {file_name}")
    else:
        print(f"Поток {thread_name} не смог скачать файл с {url}")

def download_files(urls):
    '''
    Загружает файлы из списка URLs параллельно с помощью многопоточности.
    
    Parameters:
        urls (list): Список URL-ов для загрузки
    '''
    threads = []
    
    for i, url in enumerate(urls):
        thread_name = f"Thread-{i+1}"
        
        thread = threading.Thread(target=download_file, args=(url, thread_name), name=thread_name)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

image_urls = [
    "https://picsum.photos/4000/4000",
    "https://picsum.photos/200/200",
    "https://picsum.photos/700/1300"
    
]

def make_request(url, thread_name):
    '''
    Выполняет HTTP запрос по указанному URL.
    
    Parameters:
        url (str): URL для выполнения запроса
        thread_name (str): Имя потока
    '''
    try:
        print(f"Поток {thread_name} выполняет запрос к {url}")
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"Поток {thread_name} получил успешный ответ с {url} (код {response.status_code})")
        else:
            print(f"Поток {thread_name} получил ошибку при запросе к {url} (код {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Поток {thread_name} не смог выполнить запрос к {url}. Ошибка: {e}")


def perform_requests(urls):
    '''
    Выполняет HTTP запросы для списка URLs параллельно с помощью многопоточности.
    
    Parameters:
        urls (list): Список URL-ов для запросов
    '''
    threads = []
    
    for i, url in enumerate(urls):
        thread_name = f"Thread-{i+1}"
        
        thread = threading.Thread(target=make_request, args=(url, thread_name), name=thread_name)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        
site_urls= [
    "https://www.google.com",
    "https://www.example.com",
    "https://dant4ick.ru/tgtest"
]

def factorial(n, thread_name):
    '''
    Вычисляет факториал числа n.

    Parameters:
        n (int): Число, для которого нужно вычислить факториал
        thread_name (str): Имя потока
    '''
    print(f"Поток {thread_name} начал вычисление факториала для числа {n}")
    result = math.factorial(n)
    print(f"Поток {thread_name} завершил вычисление: факториал {n} = {result}")
    
def compute_factorials(numbers):
    '''
    Вычисляет факториалы для списка чисел параллельно с помощью многопоточности.

    Parameters:
        numbers (list): Список чисел, для которых нужно вычислить факториал
    '''
    threads = []
    
    for i, number in enumerate(numbers):
        thread_name = f"Thread-{i+1}"
        thread = threading.Thread(target=factorial, args=(number, thread_name), name=thread_name)
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()
        
to_factorial =[5, 7, 2, 12, 11]

def quicksort(arr, low, high, thread_name):
    '''
    Реализует быструю сортировку на подмассиве arr[low..high].

    Parameters:
        arr (list): Список для сортировки
        low (int): Индекс начала подмассива
        high (int): Индекс конца подмассива
        thread_name (str): Имя потока
    '''
    if low < high:
        pivot = partition(arr, low, high)
        
        left_thread = threading.Thread(target=quicksort, args=(arr, low, pivot-1, f"{thread_name}_left"))
        right_thread = threading.Thread(target=quicksort, args=(arr, pivot+1, high, f"{thread_name}_right"))
        
        left_thread.start()
        right_thread.start()
        
        left_thread.join()
        right_thread.join()

def partition(arr, low, high):
    '''
    Разделяет массив на две части для быстрой сортировки и возвращает индекс опорного элемента.

    Parameters:
        arr (list): Список для сортировки
        low (int): Индекс начала подмассива
        high (int): Индекс конца подмассива
    '''
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1

def parallel_quicksort(arr):
    '''
    Запускает многопоточную быструю сортировку для всего массива.

    Parameters:
        arr (list): Список для сортировки
    '''
    thread_name = "Thread-1"
    quicksort(arr, 0, len(arr)-1, thread_name)
    
arr = [10, 7, 8, 9, 1, 5, 3, 2, 4, 6]

if __name__ == "__main__":
    download_files(image_urls)
    print()
    perform_requests(site_urls)
    print()
    compute_factorials(to_factorial)
    print()
    parallel_quicksort(arr)
