import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

url = 'https://vtomske.ru/tag/economics'
current_url = url


links_list = [url]
titles_list = []


def decorator(func):
    def wrapper(*args, **kwargs):
        print('Выполняем функцию...')
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f'Функция выполнена за {total_time} секунд.')
        return result

    return wrapper


# Создаем сессию с повторными попытками
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_titles(page_url):
    try:
        response = session.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        titles = soup.find_all('div', class_=lambda x: x and 'lenta_material_title' in x)

        for title in titles:
            title_text = title.get_text(strip=True)
            titles_list.append(title_text)
            print(title_text)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе {page_url}: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")


@decorator
def paginator():
    global current_url
    count = 1

    while True:
        print(f"\nПарсим страницу {count}: {current_url}")
        get_titles(current_url)

        try:
            response = session.get(current_url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'lxml')
            page = soup.find('a', class_=lambda x: x and 'btn lenta_pager_next' in x)

            if not page:
                print("Следующая страница не найдена. Завершаем пагинацию.")
                break

            page_href = page.get('href')
            if not page_href:
                print("Ссылка на следующую страницу пуста. Завершаем пагинацию.")
                break

            current_url = url + page_href

            if current_url in links_list:
                print("Обнаружена повторяющаяся страница. Завершаем пагинацию.")
                break

            links_list.append(current_url)
            count += 1
            time.sleep(3)

        except Exception as e:
            print(f"Ошибка: {e}")
            break

    data = []
    for i, title in enumerate(titles_list, 1):
        data.append({
            'number': i,
            'title': title
        })

    return pd.DataFrame(data)


# Запускаем
try:
    df = paginator()
    print(f"\nВсего собрано заголовков: {len(df)}")
    print(df.head())

    df.to_csv('vtomske_titles.csv', index=False, sep=';', encoding='utf-8-sig')
    print("Файл успешно сохранен!")

except Exception as e:
    print(f"Критическая ошибка: {e}")