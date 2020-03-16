import requests
from bs4 import BeautifulSoup
import json

result = []
renane_work_hours = lambda x: x.replace(':', '', 1).replace('-', ' - ', 1)

r = requests.get('https://www.mebelshara.ru/contacts')
soup = BeautifulSoup(r.content, 'html.parser')

city_item = soup.find_all('div', class_='city-item')
for city in city_item:
    for shop in city.find_all('div', 'shop-list-item'):
        if "Без выходных" in shop.attrs['data-shop-mode1']:
            working_hours = ['пн - вс {}'.format(shop.attrs['data-shop-mode2'])]
        else:
            working_hours = [
                renane_work_hours(shop.attrs['data-shop-mode1']),
                renane_work_hours(shop.attrs['data-shop-mode2']),
            ]
        result.append({
            "address": '{}, {}'.format(
                city.find('h4').text,
                shop.attrs['data-shop-address']),
            "latlon": [
                shop.attrs['data-shop-latitude'],
                shop.attrs['data-shop-longitude'],
            ],
            "name": shop.attrs['data-shop-name'], # Мебель Шара Question
            "phones": ["8 800 551 06 10"],
            "working_hours": working_hours
        })
        
with open('data/mebelshara_contacts.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)