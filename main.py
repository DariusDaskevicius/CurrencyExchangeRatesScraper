import requests
import json
from bs4 import BeautifulSoup

HOST = 'https://www.seb.lt'
URL = 'https://www.seb.lt/eng/exchange-rates'
HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36'
}

def save_json(items):
    with open('ExchangeRates.json', 'w', encoding='utf-8') as json_file:
        json.dump(items, json_file, indent=4, ensure_ascii=False)

def get_htm(url, params=''):
    request = requests.get(url, headers=HEADERS, params=params)
    return request

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('tr', class_='crc-row')
    data = []

    for item in items:
        currency = item.find(class_='flag')
        transfer_buys = item.select('td', class_='right nowrap mobile-hide')[2]
        ecb_rate = item.select('td', class_='right nowrap mobile-hide')[3]

        data.append({
            'Currency': currency.next_sibling.strip(),
            'Transfer sells': item.find('td', class_='right nowrap mobile-hide').get_text(),
            'Transfer buys': transfer_buys.get_text(strip=True),
            'ECB Rate': ecb_rate.get_text(strip=True)
        })
    return data

def parser():
    html = get_htm(URL)
    if html.status_code == 200:
        ExchangeRates = []
        ExchangeRates.extend(get_content(html.text))
        save_json(ExchangeRates)
    else:
        print('Error')

parser()