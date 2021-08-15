import os
import requests
from bs4 import BeautifulSoup
from collections import Counter

from threading import Thread
import csv
import time

import randomuseragent
import proxylist

alpha = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]

_authorUrl = []


def getAllAuthorUrl(alpha, page):
    prox = {
        'http': proxylist.proximizer(),
        'https': proxylist.proximizer()
    }
    headers = {'User-Agent': randomuseragent.GET_UA()}

    page = requests.get(
        'https://www.brainyquote.com/authors/'+alpha+str(page), headers=headers, proxies=prox)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find(
        "table", {"class": "table table-hover table-bordered"}).findAll("a")

    for aurl in table:
        _authorUrl.append(
            "https://www.brainyquote.com" + aurl.get("href"))

    return(_authorUrl)


def checkPageNum(p, l):
    prox = {
        'http': proxylist.proximizer(),
        'https': proxylist.proximizer()
    }
    headers = {'User-Agent': randomuseragent.GET_UA()}

    page = requests.get(
        'https://www.brainyquote.com/authors/'+str(p)+str(l), headers=headers, proxies=prox)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        pages = soup.find(
            "ul", {"class": "pagination bqNPgn pagination-sm"}).findAll("li")

        if pages[len(pages) - 1].find('a'):
            return 1
        else:
            return 0
    except:
        getAuthorUrlList2(p)
        return 0


def getAuthorUrlList():
    i = 0
    j = 0
    while j < len(alpha):
        while checkPageNum(alpha[j], i) == 1:
            data = getAllAuthorUrl(alpha[j], i)

            with open('authorlist.csv', 'w') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter='\n')
                wr.writerow(data)
            i += 1
            print("url downloaded from page "+alpha[j] + " page " + str(i))
        j += 1
        i = 0


def getAuthorUrlList2(alpha):
    i = 1
    data = getAllAuthorUrl(alpha, i)

    with open('authorlist.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter='\n')
        wr.writerow(data)

    print("url downloaded from page "+alpha + " page " + str(i))


allQuotes = []


def getProjectDetails(url, p):
    prox = {
        'http': proxylist.proximizer(),
        'https': proxylist.proximizer()
    }
    headers = {'User-Agent': randomuseragent.GET_UA()}

    page = requests.get(url+"_"+str(p), headers=headers, proxies=prox)
    soup = BeautifulSoup(page.content, 'html.parser')

    quotedata = soup.findAll(
        "div", {"class": "grid-item qb clearfix bqQt b-qt-lg"})

    authodetails = soup.find("div", {"class": "subnav-below-p"}).findAll("a")

    try:
        _country = authodetails[0].text
        _type = authodetails[1].text
        _born = authodetails[2].text
        _died = authodetails[3].text
    except:
        _country = ""
        _type = ""
        _born = ""
        _died = ""

    for qdata in quotedata:
        _quote = qdata.find("a", {"title": "view quote"}).text
        _author = qdata.find("a", {"title": "view author"}).text
        categories = qdata.findAll("a", {"class": "qkw-btn"})
        category = []

        for cat in categories:
            category.append(cat.text)

        data = {
            "quote": _quote,
            "author": _author,
            "country": _country,
            "profession": _type,
            "born": _born,
            "died": _died,
            "categories": category
        }

        allQuotes.append(data)

        with open('quotesnew.csv', 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter='\n')
            wr.writerow(allQuotes)

    return allQuotes


def checkPageQuotesPageNum(url, p):
    prox = {
        'http': proxylist.proximizer(),
        'https': proxylist.proximizer()
    }
    headers = {'User-Agent': randomuseragent.GET_UA()}

    page = requests.get(str(url)+'_'+str(p), headers=headers, proxies=prox)

    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        pages = soup.find(
            "ul", {"class": "pagination bq_pageNumbers pagination-centered pagination-sm"}).findAll("a")

        i = 0
        if pages:
            while i < len(pages):
                getProjectDetails(url, i)
                time.sleep(3)
                print("downloading "+url+"_"+str(i+1))
                i += 1
    except:
        getProjectDetails(url, 1)
        time.sleep(3)
        print("downloading "+url)


def getAuthorQuotes():
    with open('authorlist.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')

        threadlist = []

        for row in csv_reader:
            t = Thread(target=checkPageQuotesPageNum, args=(row[0], 1))
            t.start()
            time.sleep(3)
            threadlist.append(t)

        for b in threadlist:
            if b.is_alive():
                print('Still running')
            else:
                b.terminate()
                print('Completed')
                b.join()


if os.path.isfile('authorlist.csv'):
    print("file exist. Loading data from file.")
    getAuthorQuotes()


else:
    print("file does not exist. Getting data from website")
    getAuthorUrlList()
