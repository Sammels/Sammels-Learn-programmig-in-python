# Проведено в учебных целях

import requests
from bs4 import BeautifulSoup as bs


def get_html(url: str) -> str:
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequstException, ValueError):
        print('Сетевая ошибка')
        return False

def get_python_news()-> list:
    html = get_html("https://www.python.org/blogs/")
    if html:
        soup = bs(html, 'html.parser')
        all_news = soup.find('ul', class_='list-recent-posts').findAll('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text
            result_news.append({
                "title": title,
                "url": url,
                "published": published
            })
        return result_news
    return False
