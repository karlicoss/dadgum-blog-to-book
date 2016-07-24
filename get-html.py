#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests


URL = "http://prog21.dadgum.com/"


def strip_page(soup):
    # remove section on the right
    soup.find(id='c2').extract()
    prev = soup.find(text='previously')
    if prev is not None:
        prev.parent.parent.extract()
    soup.find(id='top').extract()


def process_index_page(soup):
    soup.find(id='c2').extract()
    prev = soup.find(text='previously')

    root = soup.find(class_='ab')
    children = list(root.children)
    root.clear()

    res = []
    cur_year = None
    for c in children:
        if c.name == 'h1':
            if cur_year is not None:
                res.append(cur_year)
            cur_year = c
        else:
            res.append(c)

    res.append(cur_year)

    for child in reversed(res):
        root.append(child)


soup = BeautifulSoup(requests.get(URL + "archives.html").text, 'html.parser')
process_index_page(soup)
with open('res/blog.html', 'w') as f:
    f.write(str(soup))


TOTAL_POSTS = 220

for i in range(1, TOTAL_POSTS + 1):
    print("Processing page %d" % i)
    url = "%s"URL + str(i) + ".html"
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    strip_page(soup)
    with open('res/%d.html' % i, 'w') as f:
        f.write(str(soup))
