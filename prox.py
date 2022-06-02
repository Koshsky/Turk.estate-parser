from random import choice


with open('proxies_IPv4_socks5.txt', 'r') as file:
    proxies_IPv4_socks5 = [line.strip() for line in file.readlines()]


def get_random_IPv4_socks5(protocol=True):
    ip = choice(proxies_IPv4_socks5)
    return  'socks5://'*protocol + ip
