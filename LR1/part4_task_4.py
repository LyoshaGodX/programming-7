import asyncio
import aiohttp
import asyncpg
import json
from aiohttp import ClientSession
from datetime import datetime
from termcolor import colored

WEB_SERVER_URL = "https://rnacentral.org/api/v1/rna/"
DB_CONNECTION_STRING = "postgres://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"


def shorten_text(text, length=100):
    """
    Урезает текст до указанного количества символов, добавляя '...'.
    """
    return text[:length] + "..." if len(text) > length else text

def format_http_result(http_result):
    """
    Форматирует и сокращает данные HTTP-ответа.
    """
    if not http_result:
        return "Нет данных HTTP-запроса."
    
    formatted_result = {
        "URL": http_result.get("url"),
        "RNA ID": http_result.get("rnacentral_id"),
        "Description": http_result.get("description"),
        "Sequence (shortened)": shorten_text(http_result.get("sequence", ""), 50),
        "Length": http_result.get("length"),
        "Databases": http_result.get("distinct_databases", [])
    }
    return json.dumps(formatted_result, indent=4, ensure_ascii=False)

def format_db_results(db_results):
    """
    Форматирует и сокращает данные из базы.
    """
    if not db_results:
        return "Нет данных из базы данных."

    formatted_list = []
    for row in db_results:
        formatted_row = {
            "ID": row.get("id"),
            "Name": row.get("full_descr", "Unknown"),
            "Description": shorten_text(row.get("description", ""), 50),
            "URL": row.get("url"),
            "Alive": row.get("alive", "Unknown"),
            "Avg Length": row.get("avg_length"),
            "Num Sequences": row.get("num_sequences"),
        }
        formatted_list.append(formatted_row)
    
    return json.dumps(formatted_list, indent=4, ensure_ascii=False)

async def fetch_http_data(session: ClientSession, url: str):
    """
    Выполняет HTTP-запрос к указанному URL и возвращает результат.
    """
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = await response.json()
            print("HTTP-запрос выполнен успешно!")
            return data
    except Exception as e:
        print(f"Ошибка HTTP-запроса: {e}")
        return None


async def fetch_db_data():
    """
    Выполняет запрос к базе данных и возвращает данные.
    """
    try:
        conn = await asyncpg.connect(DB_CONNECTION_STRING)
        query = "SELECT * FROM rnc_database LIMIT 3;"
        data = await conn.fetch(query)
        await conn.close()
        print("Запрос к базе данных выполнен успешно!")
        return [dict(row) for row in data]
    except Exception as e:
        print(f"Ошибка запроса к базе данных: {e}")
        return None


def handle_datetime(obj):
    """
    Обработчик для преобразования datetime в строку, иначе райзит ошибку при сериализации в джейсон.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


async def process_results(results):
    """
    Обрабатывает и печатает результаты.
    """
    print("\n" + colored("Обработка результатов:", "cyan", attrs=["bold"]))

    http_result = results.get("http")
    print("\n" + colored("Результат HTTP-запроса:", "green", attrs=["bold"]))
    print(format_http_result(http_result))

    db_result = results.get("db")
    print("\n" + colored("Результат запроса к базе данных:", "blue", attrs=["bold"]))
    print(format_db_results(db_result))


async def main():
    """
    Основная асинхронная функция.
    """
    async with aiohttp.ClientSession() as session:
        http_task = fetch_http_data(session, f"{WEB_SERVER_URL}URS0000001C34")
        db_task = fetch_db_data()

        results = await asyncio.gather(http_task, db_task)

        processed_results = {
            "http": results[0],
            "db": results[1]
        }

        await process_results(processed_results)


if __name__ == "__main__":
    asyncio.run(main())
