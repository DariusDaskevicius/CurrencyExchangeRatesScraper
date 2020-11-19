import requests
import json
from bs4 import BeautifulSoup

HOST = 'https://www.seb.lt'
URL = 'https://www.seb.lt/eng/exchange-rates'
HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36'
}

def get_htm(url, params=''):
    request = requests.get(url, headers=HEADERS, params=params)
    return request

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('tr', class_='crc-row')
    data = []

    for item in items:
        currency = item.find(class_='flag')

        data.append({
            'Currency': currency.next_sibling.strip(),
            'Transfer sells': item.find('td', class_='right nowrap mobile-hide').get_text(),
            'Transfer buys': item.find('td', class_='right nowrap mobile-hide').next_element.get_text(), # stopped here!!! 
            'ECB Rate': item.find('td', class_='right nowrap mobile-hide').get_text()
        })
    print(data)

html = get_htm(URL)



print(get_content(html.text))