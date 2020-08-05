import requests
from bs4 import BeautifulSoup


URL = 'https://www.jib.co.th/web/product/product_search '
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'accept': '*/*'}
HOST = 'https://www.jib.co.th'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='reladiv')

    products = []
    for item in items:
        old_price = item.find('span', class_='price')
        if old_price:
            old_price = old_price.get_text().replace('.-', '')
        else:
            old_price = ''
        products.append({
            'title': item.find('span', class_='promo_name').get_text(),
            'description': item.find('p', class_='mar-0 f-13').get_text(),
            'link_img': HOST + item.find('img', class_='img-responsive imgpspecial').get('src'),
            'price': item.find('p', class_='price_total').get_text().replace('.-', '').replace('\n', ''),
            'old_price': old_price,
        })
    print(products)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
       get_content(html.text)
    else:
        print('Error')

parse()
