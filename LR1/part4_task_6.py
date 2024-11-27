import aiohttp
import asyncio
import json
from aiohttp import ClientSession


class AsyncWebScraper:
    def __init__(self, urls_file: str, output_file: str):
        """
        Инициализация скрапера.
        :param urls_file: Путь к файлу с URL.
        :param output_file: Путь для сохранения результатов.
        """
        self.urls_file = urls_file
        self.output_file = output_file
        self.urls = []
        self.results = []

    async def __aenter__(self):
        """
        Асинхронная инициализация: загрузка URL из файла.
        """
        self.urls = await self._load_urls()
        print(f"Загружено {len(self.urls)} URL для скрапинга.")
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Закрытие асинхронной сессии и сохранение результатов.
        """
        await self.session.close()
        await self._save_results()
        if exc_type:
            print(f"Произошла ошибка: {exc_val}")
        print("Результаты сохранены в", self.output_file)

    async def _load_urls(self) -> list:
        """
        Загрузить URL из текстового файла.
        :return: Список URL.
        """
        try:
            with open(self.urls_file, "r") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Файл {self.urls_file} не найден.")
            return []

    async def _save_results(self):
        """
        Сохранить результаты в JSON-файл.
        """
        with open(self.output_file, "w", encoding="utf-8") as file:
            json.dump(self.results, file, indent=4, ensure_ascii=False)

    async def fetch_url(self, url: str) -> dict:
        """
        Получить содержимое веб-страницы.
        :param url: URL для запроса.
        :return: Результат с URL и статусом.
        """
        try:
            async with self.session.get(url) as response:
                content = await response.text()
                return {"url": url, "status": response.status, "content": content[:200]}
        except Exception as e:
            return {"url": url, "error": str(e)}

    async def scrape(self):
        """
        Основная функция для скрапинга всех URL.
        """
        tasks = [self.fetch_url(url) for url in self.urls]
        self.results = await asyncio.gather(*tasks)


async def main():
    """
    Основная асинхронная функция для запуска скрапера.
    """
    urls_file = "LR1/urls.txt"
    output_file = "LR1/results_async.json"

    async with AsyncWebScraper(urls_file, output_file) as scraper:
        await scraper.scrape()


if __name__ == "__main__":
    asyncio.run(main())
