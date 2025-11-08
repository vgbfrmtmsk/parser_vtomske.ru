import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

url = 'https://vtomske.ru/tag/economics'
current_url = url

page_links = {
    'link': [url]
}
title_links = {
    'title': []
}

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

# Добавляем заголовки
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_titles(page_url):
    try:
        response = session.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        titles = soup.find_all('div', class_=lambda x: x and 'lenta_material_title' in x)

        title_texts = []
        for title in titles:
            title_text = title.get_text(strip=True)
            title_texts.append(title_text)
            title_links['title'].append(title_text)
            print(title_text)

        return title_texts

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе {page_url}: {e}")
        return []
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return []


def paginator():
    global current_url
    count = 1

    while True:
        print(f"\nПарсим страницу {count}: {current_url}")

        # Парсим заголовки с текущей страницы
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

            if current_url in page_links['link']:
                print("Обнаружена повторяющаяся страница. Завершаем пагинацию.")
                break

            page_links['link'].append(current_url)
            count += 1

            # Увеличиваем задержку
            time.sleep(3)  # 3 секунды между запросами

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при пагинации: {e}")
            break
        except Exception as e:
            print(f"Общая ошибка: {e}")
            break

    # Создаем DataFrame с заголовками
    df_titles = pd.DataFrame(title_links)
    return df_titles


# Запускаем
try:
    df = paginator()
    print(f"\nВсего собрано заголовков: {len(df)}")
    print(df)

    # Сохраняем в CSV файл
    df.to_csv('vtomske_titles.csv', index=False, encoding='utf-8-sig')
    print(f"Файл 'vtomske_titles.csv' успешно сохранен!")

except Exception as e:
    print(f"Критическая ошибка: {e}")
    # Сохраняем то, что успели собрать
    if title_links['title']:
        df_titles = pd.DataFrame(title_links)
        df_titles.to_csv('vtomske_titles_partial.csv', index=False, encoding='utf-8-sig')
        print(f"Сохранены частичные результаты ({len(df_titles)} заголовков)")