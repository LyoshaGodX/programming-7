import asyncio

async def task_1():
    print("Задача 1 началась...")
    await asyncio.sleep(2)
    print("Задача 1 завершена!")
    return "Результат задачи 1"

async def task_2():
    print("Задача 2 началась...")
    await asyncio.sleep(3)
    print("Задача 2 завершена!")
    return "Результат задачи 2"

async def process_results(results):
    print("Обработка результатов началась...")
    for result in results:
        print(f"Обработан результат: {result}")
    print("Обработка результатов завершена!")

async def main():
    results = await asyncio.gather(task_1(), task_2())

    await process_results(results)

if __name__ == "__main__":
    asyncio.run(main())
