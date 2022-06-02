from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
from datetime import datetime
from prox import *
import requests
import os


class TurkEstateScraper:
    LOCATIONS = ['South',
                 'West',
                 'East',
                 'Aegen coast',
                 'Mediterranean coast']
    LOCATIONS_URL = ['https://turk.estate/en/south/',
                     'https://turk.estate/en/west/',
                     'https://turk.estate/en/east/',
                     'https://turk.estate/en/aegean-coast/',
                     'https://turk.estate/en/mediterranean-coast/']
    RESULT_HEADERS = ['Site', 'Name', 'Price',
               'City', 'Disctrict', 'Region', 'Type', 'Rooms',
               'Living space', 'To sea', 'To city center',
               'Location', 'Features', 'Indoor facilities',
               'Outdoor features', 'Property description', 'Date', 'URL']
    SITE = 'turk.estate'

    
    def __init__(self, filename, flag, from_location, from_page):
        self.filename = filename
        self.encoding = 'utf-8-sig'
        self.flag = flag
        self.ua = UserAgent()
        self.date = datetime.now().date().strftime('%Y-%m-%d')
        while self.LOCATIONS[0] != from_location:
            del self.LOCATIONS[0]
            del self.LOCATIONS_URL[0]
        self.from_location = from_location
        self.from_page = from_page
        
    def make_soup(self, url):
        headers = {'user-agent': self.ua.random}
        proxy = get_random_IPv4_socks5()
        r = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy})
        if r.status_code != 200:
            print(f"""Статус код - {r.status_code}\nИспользумый прокси: {proxy}""")
            if not os.path.exists('reports.txt'):
                with open('reports.txt', 'w'): pass
            with open('reports.txt', 'a', encoding='utf-8') as file:
                file.write(f"""{datetime.now()}\nСтатус код - {r.status_code}\nИспользумый прокси: {proxy}\n""")
        else:
            r.encoding = 'utf-8'
            return BS(r.text, 'lxml')
    
    def get_all_card_urls_by_location(self, location):
        main_url = self.LOCATIONS_URL[self.LOCATIONS.index(location)]
        main_page = self.make_soup(main_url)
        try:
            last_page = main_page.find('ul', class_='pagination').find_all('li')[-2].text
        except:
            last_page = 1
            
        start = self.from_page if self.from_location == location else 1
        for i in range(start, int(last_page)+1):
            url = f'{main_url}page/{i}/#objects'
            page = self.make_soup(url)
            for el in page.find('div', 'objects-list').find_all('div', 'image'):
                if el.find('div', 'price').find('span').text != 'Sold out':
                    card_url = el.find('a')['href']
                    yield card_url
            print(f'страница №{i} обработана.')
                
    def parse_card(self, card_url, location):
        def validate_str(s):
            return s.replace('\n', ' ').replace(';', '.')
        
        def get_name_by_selector(card, selector):
            sub = card.select(selector)
            return validate_str(sub[0].text) if sub else ''

        
        card = self.make_soup(card_url)
        
        name = validate_str(card.find('h1', {'itemprop':'name'}).text)
        price = validate_str(card.select('.main_image .price meta')[0]['content'])
        article = card.select('body > div.superwrapper > div.main-holder > div.container.object > div.row > div.page_content > div.article')
        property_description = validate_str(article[0].text).replace('Property description', '') if article else ''
        
        right_block = card.select('div.right_block.parameters')[0]
        city = get_name_by_selector(right_block, 'div.city .value')
        discrict = get_name_by_selector(right_block, 'div.region .value')
        type_ = get_name_by_selector(right_block, 'div.tip span.value')
        rooms = get_name_by_selector(right_block, 'div.rooms span.value')
        living_space = get_name_by_selector(right_block, 'div.square span.value').replace('2m', '2 m')
        to_sea = get_name_by_selector(right_block, 'div.tosea span.value')
        to_city_center = get_name_by_selector(right_block, 'div.tocenter span.value')

        d = {'location': '',
             'features': '',
             'indoor_facilities': '',
             'outdoor_features': ''}
        
        for block in card.select('.features.wrapped'):
            d[block.find('h3').text.lower()] = ', '.join(validate_str(i.text) for i in block.find_all('li'))
                
        return [self.SITE, name, price, city, discrict, location, type_, rooms,
                living_space, to_sea, to_city_center, d['location'], d['features'],
                d['indoor_facilities'], d['outdoor_features'], property_description, self.date, card_url]
    

        
    def start_parsing(self):
        if self.flag == 'w':
            with open(self.filename, 'w', newline='', encoding=self.encoding) as file:
                file.write(';'.join(self.RESULT_HEADERS)+'\n')
        
        
        for location in self.LOCATIONS:
            print(location)
            for card_url in self.get_all_card_urls_by_location(location):
                try:
                    with open(self.filename, 'a', newline='', encoding=self.encoding) as file:
                        file.write(';'.join(self.parse_card(card_url, location))+'\n')
                except Exception as _ex:
                    pass
