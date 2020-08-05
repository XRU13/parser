import requests
from bs4 import BeautifulSoup


URL = 'https://www.jib.co.th/web/product/product_search' #урл страницы, котоорую парсим
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'accept': '*/*'} #берем заголовки, чтобы сервер нас не банил как скрипт
HOST = 'https://www.jib.co.th' #добаваляем хост к ссылке на фото, для кликабельности

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser') #библиотека для того чтобы парсить
    items = soup.find_all('div', class_='reladiv') #находим карточку товара и вытаскиваем из нее нужные нам элементы

    products = []
    for item in items:
        old_price = item.find('span', class_='price') #проверяем есть ли старая цена
        if old_price:
            old_price = old_price.get_text().replace('.-', '') #если есть, берем из нее текст
        else:
            old_price = ''#если нет, ничего не берем
        products.append({ #создаем библиотеку
            'title': item.find('span', class_='promo_name').get_text(), #находим заголовок
            'description': item.find('p', class_='mar-0 f-13').get_text(), #находим описание
            'link_img': HOST + item.find('img', class_='img-responsive imgpspecial').get('src'), #находим урл фотки и добавляем хост для кликабельности
            'price': item.find('p', class_='price_total').get_text().replace('.-', '').replace('\n', ''), #находим цену
            'old_price': old_price, #находим старую цену
        })
    print(products) #печатаем все что нашли


def parse():
    html = get_html(URL)
    if html.status_code == 200: #если сайт отвечает код 200, то запрашиваем html
       get_content(html.text)
    else: #если нет, пишем ошибку
        print('Error')

parse()
