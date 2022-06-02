# Turk.estate-parser
Parser turk.estate
Собирает ифнормацию о каждом объявлении продажи недвижимости с сайта turk.estate
Информация сохраняется в .csv формате с разделителем ;

столбцы:
  Site
  Name
  Price
  City
  Disctrict
  Region
  Type
  Rooms
  Living space
  To sea
  To city center
  Location
  Features
  Indoor facilities
  Outdoor features
  Property description	
  Date	
  URL

  
Все исползуемые библиотеки: 

random
fake_useragent
bs4
datetime
requests
os

Это нужно ввести в коммандную строку (Win+R->ввести "cmd"-> командная строка открыта!):

pip install beautifulsoup4
pip install fake-useragent
pip install lxml
pip instal pysocks (бывают проблемы без этой команды)


  Файл proxies_IPv4_socks5.txt нужно наполнить вашими прокси по образцу. если ваш прокси
не предусматривает использование логина и пароля, то используется формат ip:port
  Бесплатные прокси можно найти здесь: https://hidemy.name/ru/proxy-list/
  В reports.txt логируются зафиксированные ошибки с прокси


Контакты:
Телеграм: @Koshsky
Степик: https://stepik.org/users/142796504
Вконтакте: https://vk.com/koshsky_1
