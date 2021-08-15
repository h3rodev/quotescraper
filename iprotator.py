import requests
from bs4 import BeautifulSoup
import randomuseragent
import proxylist
import time
import random

_proxylist = open('iplist.txt', 'r')
listcount = _proxylist.readlines()


def get_proxies():
    prox = {
        'https': proxylist.proximizer()
    }
    headers = {'User-Agent': randomuseragent.GET_UA()}

    url = 'https://inspiresean.com'

    r = requests.get(url, headers=headers, proxies=prox)
    page = BeautifulSoup(r.content, 'html.parser')

    return page.find("title")


i = 0
while i < 20:
    try:
        print(get_proxies())
        time.sleep(random.randint(1, 5))
    except:
        print("error loading")
    i += 1
