import asyncio
import time
from termcolor import colored
from pynput import keyboard

exit_program = False

def on_press(key):
    """Обработчик для нажатия клавиши."""
    global exit_program
    try:
        if key == keyboard.Key.esc:
            exit_program = True
    except AttributeError:
        pass

async def display_time():
    """Асинхронная функция, которая будет выводить дату и время каждую секунду."""
    global exit_program
    while not exit_program:
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y-%m-%d")

        print(colored(f"{current_date} {current_time}", "yellow"), end="\r")

        await asyncio.sleep(1)

def start_listener():
    """Функция для прослушивания нажатий клавиш с использованием pynput."""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

async def main():
    """Главная асинхронная функция для запуска программы."""
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, start_listener)
    
    await display_time()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")
