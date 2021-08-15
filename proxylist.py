import random

proxylist = open('iplist.txt', 'r')
proxies = proxylist.readlines()


def proximizer():
    plist = []
    count = 0
    # Strips the newline character
    for proxy in proxies:
        count += 1
        _p = proxy.strip().split()
        _fp = 'http://{}:{}'.format(_p[0], _p[1])
        plist.append(_fp)

    return(plist[random.randint(len(proxies)/2, len(proxies))])
