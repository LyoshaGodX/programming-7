import asyncio
import time

async def display_time():
    """Асинхронная функция, которая будет выводить текущее время каждую секунду."""
    while True:
        current_time = time.strftime("%H:%M:%S")
        print(f"Текущее время: {current_time}")
        await asyncio.sleep(1)

async def main():
    """Главная асинхронная функция для запуска программы."""
    await display_time()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")