import aiohttp
import asyncio
from aiohttp import ClientSession
from termcolor import colored

class AsyncWebScraper:
    def __init__(self, urls, concurrency=5):
        """
        Инициализация скрапера.
        :param urls: Список URL для скрапинга.
        :param concurrency: Максимальное количество одновременных запросов.
        """
        self.urls = urls
        self.concurrency = concurrency
        self.results = []

    async def fetch(self, session: ClientSession, url: str):
        """
        Выполняет запрос к указанному URL.
        :param session: Сессия aiohttp.
        :param url: Адрес для запроса.
        """
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    print(colored(f"Успешно загружено: {url}", "green"))
                    return {"url": url, "content": text[:200]}
                else:
                    print(colored(f"Ошибка {response.status} при загрузке: {url}", "red"))
                    return {"url": url, "error": response.status}
        except Exception as e:
            print(colored(f"Ошибка при запросе к {url}: {e}", "red"))
            return {"url": url, "error": str(e)}

    async def scrape(self):
        """
        Основной метод скрапера, который обрабатывает список URL.
        """
        semaphore = asyncio.Semaphore(self.concurrency)
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._bounded_fetch(semaphore, session, url)
                for url in self.urls
            ]
            self.results = await asyncio.gather(*tasks)

    async def _bounded_fetch(self, semaphore, session, url):
        """
        Обеспечивает ограничение одновременных запросов.
        """
        async with semaphore:
            return await self.fetch(session, url)

    def save_results(self, file_name="LR1/results.json"):
        """
        Сохраняет результаты в файл.
        :param file_name: Имя файла для сохранения.
        """
        import json
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
        print(colored(f"Результаты сохранены в {file_name}", "blue"))

def load_urls(file_name="LR1/urls.txt"):
    """
    Загружает список URL из файла.
    :param file_name: Имя файла.
    :return: Список URL.
    """
    with open(file_name, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

async def main():
    urls = load_urls()
    print(f"Загружено {len(urls)} URL для скрапинга.")
    scraper = AsyncWebScraper(urls, concurrency=5)
    await scraper.scrape()
    scraper.save_results()

if __name__ == "__main__":
    asyncio.run(main())