from turk_estate_scraper import TurkEstateScraper as TS


if __name__ == '__main__':
    ban_symbols = ('+','=','[',']',':',';','«',',','.','/','?',' ',r'/','\\',':','*','?','«','<','>','|',)

    
    filename = input("Введите имя файла, куда сохранить результат: ")
    while any(i in ban_symbols for i in filename):
        filename = input("Имя файла не должно содержать символы +=[]:;«,./?'пробел'/\:*? «<>|: ")
    filename += '.csv'

              
    flag = input(f"""Введите 'a', если {filename} необходимо дополнить новыми значениями
Введите 'w' если {filename} необходимо создать или заполнить заново: """).lower()
    while flag not in ('a', 'w'):
        flag = input("Пожалуйста введите или 'a' или 'w': ").lower()

    from_location = input("""'South', 'West', 'East', 'Aegen coast', 'Mediterranean coast'
Введите 'South', если парсить нужно нужно все локации.
'West', если начать парсинг необходимо с 'West'.
'East', если с 'East',
'Aegen coast, если c 'Aegen coast',
'Mediterranean coast', если с 'Mediterranean coast':
""").capitalize()
    while from_location not in ['South', 'West', 'East', 'Aegen coast', 'Mediterranean coast']:
        from_location = input('Пожалуйста введите корректное значение: ').capitalize()

    from_page = input('Введите номер страницы, с которой начать парсинг: ')
    while not from_page.isdigit():
        from_page = input('Пожалуйста введите целое число: ')
    from_page = int(from_page)

    parser = TS(filename, flag, from_location, from_page)
    parser.start_parsing()
    print('СКРИПТ ЗАВЕРШИЛ РАБОТУ. ВСЕ ДАННЫЕ О ПРОДАЖАХ НЕДВИЖИМОСТИ С САЙТА TURK.ESTATE СОБРАНЫ.')
