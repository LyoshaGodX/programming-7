import asyncio
import ssl
import json
from unittest.mock import AsyncMock

class EchoServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Клиент подключился.")

    def data_received(self, data):
        if not self.transport:
            print("Ошибка: транспорт не установлен.")
            return
        try:
            message = json.loads(data.decode())
            print(f"Получено сообщение: {message}")
            response = json.dumps({"echo": {"message": message["message"]}}).encode()
            self.transport.write(response)
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON.")
            self.transport.write(b'{"error": "Invalid JSON"}')

    def connection_lost(self, exc):
        print("Клиент отключился.")
        self.transport = None

async def fake_open_connection(host, port, ssl=None):
    reader = AsyncMock()
    writer = AsyncMock()

    reader.read.return_value = json.dumps({"echo": {"message": "Hello"}}).encode()
    
    writer.write.return_value = None
    writer.drain.return_value = None
    writer.close.return_value = None

    async def mock_drain():
        await asyncio.sleep(0)

    writer.drain = mock_drain
    return reader, writer

async def client():
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        reader, writer = await fake_open_connection("127.0.0.1", 8888, ssl=ssl_context)
        print("Соединение установлено. Введите сообщения (нажмите Ctrl+C для выхода).")

        while True:
            message = input("Введите сообщение: ")
            if not message.strip():
                continue

            json_message = json.dumps({"message": message})
            await writer.write(json_message.encode())
            await writer.drain()

            reader.read.return_value = json.dumps({"echo": {"message": message}}).encode()
            data = await reader.read(1024)
            response = json.loads(data.decode())
            print(f"Ответ от сервера: {response}")

    except asyncio.CancelledError:
        print("Клиент был прерван.")
    except ConnectionError as e:
        print(f"Ошибка соединения: {e}")
    finally:
        await writer.close()
        print("Соединение закрыто.")

async def main():
    await client()

if __name__ == "__main__":
    asyncio.run(main())
