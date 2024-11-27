import concurrent.futures

def write_to_file(file_path, data):
    """
    Записывает данные в файл.

    Parameters:
        file_path (str): Путь к файлу.
        data (str): Данные для записи.
    """
    with open(file_path, 'w') as file:
        file.write(data)
    print(f"Данные записаны в файл {file_path}")

def read_from_file(file_path):
    """
    Считывает данные из файла.

    Parameters:
        file_path (str): Путь к файлу.

    Returns:
        str: Содержимое файла.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    print(f"Данные считаны из файла {file_path}: {content}")
    return content

def main():
    file_path = "example.txt"
    data_to_write = "Запись в файле"

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        write_future = executor.submit(write_to_file, file_path, data_to_write)

        read_future = executor.submit(lambda: write_future.result() or read_from_file(file_path))

        write_future.result()
        read_content = read_future.result()


if __name__ == "__main__":
    main()
