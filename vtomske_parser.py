import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


url = 'https://vtomske.ru/tag/economics'
current_url = url

title_links = {
    'link': []
}


def decorator(func):
    def wrapper(*args, **kwargs):
        print('Выполняю функцию...')
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f'Функция выполнена за {total_time:.3f} секунд.')
        return result
    return wrapper


@decorator
def get_links_of_the_page(data):
    full_links = []
    link_num = 0
    for i in data:
        href = i.get('href')
        link_num += 1
        print(f'Ссылка {link_num}: ')
        full_link = f'https://vtomske.ru{href}'
        print(full_link)
        full_links.append(full_link)
    return full_links

def paginator():
    global current_url
    for count in range(1, 5):
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'lxml')
        page = soup.find('a', class_=lambda x: x and 'btn lenta_pager_next' in x)
        if page:
            page_href = page.get('href')
            current_url = url + page_href
            print(current_url)
            title_links['link'].append(current_url)
    df = pd.DataFrame(title_links)
    return df

df = paginator()
print(df)


