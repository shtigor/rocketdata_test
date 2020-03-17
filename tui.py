import requests
import json
import time

result = []
DAY_OF_WEEKS = {
    'workdays': 'пн - пт',
    'saturday': 'сб',
    'sunday': 'вс'
}

def get_work_hours(work_hours):
    hours = []
    for h in work_hours:
        if not work_hours[h]['isDayOff']:
            start = work_hours[h]['startStr']
            end = work_hours[h]['endStr']
            hours.append(f'{DAY_OF_WEEKS[h]} {start} - {end}')

    return hours


cities = requests.get('https://www.tui.ru/api/office/cities/')
offices_url = 'https://www.tui.ru/api/office/list/?cityId={}'

cities_json = json.loads(cities.content.decode())

for city in cities_json:
    offices = requests.get(offices_url.format(city['cityId']))
    offices_json = json.loads(offices.content.decode())
    for office in offices_json:
        result.append({
            "address": office['address'],
            "latlon": [
                office['latitude'],
                office['longitude']
            ],
            "name": office['name'],
            "phones": [
                phone['phone'].strip() for phone in office['phones']
                ],
            "working_hours": get_work_hours(office['hoursOfOperation']),})
    
    time.sleep(2) # with this pause execution is approximately 5 - 6 min

with open('data/tui_contacts.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)