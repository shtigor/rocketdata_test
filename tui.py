import requests
from bs4 import BeautifulSoup
import json


cities = requests.get('https://www.tui.ru/api/office/cities/')
offices = 'https://www.tui.ru/api/office/list/?cityId={}'