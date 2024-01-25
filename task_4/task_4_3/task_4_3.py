import aiohttp
import asyncio
from time import time
import sys

async def download_image(url):
    try:
        start_time = time()  # время начала скачивания
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    filename = url.split('/')[-1]
                    with open(filename, 'wb') as f:
                        f.write(await response.read())
                    end_time = time()  # время конца скачивания
                    print(f"Изображение {filename} скачано за {end_time - start_time:.2f} секунд")
                else:
                    print(f"Ошибка при скачивании изображения {url}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения {url}: {str(e)}")

async def main():
    urls = sys.argv[1:]  # URL-адреса из аргументов командной строки
    start_time = time()
    
    tasks = [download_image(url) for url in urls]
    await asyncio.gather(*tasks)

    end_time = time()
    total_time = end_time - start_time
    print(f"Общее время выполнения программы: {total_time} секунд")

if __name__ == "__main__":
    asyncio.run(main())