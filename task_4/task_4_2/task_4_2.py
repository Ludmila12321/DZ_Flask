from requests import get
from multiprocessing import Process
from time import time
import sys

def download_image(url):
    try:
        start_time = time()  # время начала скачивания
        response = get(url)
        if response.status_code == 200:
            filename = url.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(response.content)
            end_time = time()  # время конца скачивания
            print(f"Изображение {filename} скачано за {end_time - start_time:.2f} секунд")
        else:
            print(f"Ошибка при скачивании изображения {url}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения {url}: {str(e)}")

def main():
    urls = sys.argv[1:]  # URL-адреса из аргументов командной строки

    start_time = time()

    processes = []
    for url in urls:
        process = Process(target=download_image, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time()
    total_time = end_time - start_time
    print(f"Общее время выполнения программы: {total_time} секунд")

if __name__ == "__main__":
    main()