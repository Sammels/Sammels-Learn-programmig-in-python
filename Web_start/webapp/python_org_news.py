# Проведено в учебных целях
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

from webapp.model import db, News


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
            try:
                published = datetime.strptime(published, '%Y-%m-%d')
            except(ValueError):
                published = datetime.now()
            save_news(title,url,published)


def save_news(title,url,published):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        news_news = News(title=title, url=url, published=published)
        db.session.add(news_news)
        db.session.commit()