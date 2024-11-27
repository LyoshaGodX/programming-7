import os
import threading


def create_test_directory(base_dir):
    """
    Создаёт тестовую директорию с несколькими поддиректориями и файлами теста.
    """
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    subdirs = ['subdir1', 'subdir2', 'subdir3']
    for subdir in subdirs:
        os.makedirs(os.path.join(base_dir, subdir))

    test_file_content = "Тестовый файл"
    with open(os.path.join(base_dir, 'subdir1', 'example.txt'), 'w') as f:
        f.write(test_file_content)
    with open(os.path.join(base_dir, 'subdir2', 'otherfile.txt'), 'w') as f:
        f.write("Не тот")
    with open(os.path.join(base_dir, 'subdir3', 'randomfile.txt'), 'w') as f:
        f.write("Еще один не тот")

def search_files(directory, pattern, stop_event, result, thread_name):
    """
    Параллельный поиск файлов в указанной директории.
    
    Parameters:
        directory (str): Директория для поиска.
        pattern (str): Имя файла или его часть для поиска.
        stop_event (threading.Event): Событие для остановки потоков.
        result (list): Список для хранения результата поиска.
        thread_name (str): Имя текущего потока.
    """
    print(f"[{thread_name}] Начинаю поиск в {directory}")

    try:
        for root, _, files in os.walk(directory):
            if stop_event.is_set():
                print(f"[{thread_name}] Поиск завершён (остановлен).")
                return

            for file in files:
                if pattern in file:
                    full_path = os.path.join(root, file)
                    result.append(full_path)
                    print(f"[{thread_name}] Файл найден: {full_path}")
                    stop_event.set()
                    return
    except Exception as e:
        print(f"[{thread_name}] Ошибка: {e}")

    print(f"[{thread_name}] Поиск завершён: файл не найден.")

def parallel_file_search(directory, pattern, num_threads=4):
    """
    Основная функция для параллельного поиска файла.

    Parameters:
        directory (str): Директория для поиска.
        pattern (str): Имя файла или его часть для поиска.
        num_threads (int): Количество потоков для поиска.
    """
    stop_event = threading.Event()
    result = []
    threads = []

    subdirs = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    subdirs_per_thread = max(1, len(subdirs) // num_threads)

    for i in range(num_threads):
        start = i * subdirs_per_thread
        end = None if i == num_threads - 1 else (i + 1) * subdirs_per_thread
        thread_dirs = subdirs[start:end]

        if not thread_dirs:
            thread_dirs = [directory]

        thread_name = f"Thread-{i+1}"
        thread = threading.Thread(
            target=search_files,
            args=(directory, pattern, stop_event, result, thread_name),
            name=thread_name
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    if result:
        print(f"Файл найден: {result[0]}")
    else:
        print("Файл не найден.")

if __name__ == "__main__":
    
    test_directory = "./test_dir"
    create_test_directory(test_directory)
    
    search_pattern = "example.txt"
    parallel_file_search(test_directory, search_pattern, num_threads=4)