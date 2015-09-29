# encoding=utf-8
__author__ = 'elmira'

import urllib.request as urlr
from urllib.error import HTTPError
from html import unescape
import bz2


def load_dump():
    """
    Downloads the latest dump from Wikipedia for a specified language.

    Asks user to input a language code.
    Generates a url for the dump of Wikipedia articles written in this language.
    If the code is valid, checks whether the size of the corresponding dump is greater than 50 MB.
    If so, asks for confirmation.
    Downloads and decompresses the dump file.
    """
    code = input('Input language code: ')  # ru, en, udm
    url = 'https://dumps.wikimedia.org/' + code + 'wiki/latest/' + code + 'wiki-latest-pages-articles.xml.bz2'
    try:
        page = urlr.urlopen(url)
        size = page.info().get("Content-Length")
        size_in_mb = int(size) / (1024 * 1024)
        if size_in_mb > 50:
            print("Dump size:", "{:10.3f}".format(size_in_mb), 'MB.')
            response = input('Do you still think you want to download the file? y/n: ')
            if response != 'y':
                return
        print('Downloading...')
        open(code + 'wiki-latest-pages-articles.xml.bz2', 'b+w').write(page.read())
        print('Decompressing...')
        decompressed = bz2.BZ2File(code + 'wiki-latest-pages-articles.xml.bz2').read()
        open(code + 'wiki-latest-pages-articles.xml', 'wb').write(decompressed)
        print('Done.')
        return
    except HTTPError:
        print('Page not found. No language has code "' + code + '".')
        return


def find_articles():
    """
    Prints to file the names of all articles from Wikipedia for a specified language.
    """
    code = input('Input language code: ')  # ru, en, udm
    articles = set()
    with open(code + 'wiki-latest-pages-articles.xml', 'r', encoding='utf-8') as dump:
        for line in dump:
            s = line.strip()
            if s.startswith('<title>') and s.endswith('</title>'):
                s = s.replace('<title>', '').replace('</title>', '')
                articles.add(unescape(s))
    open('article_names.txt', 'w', encoding='utf-8').write('\n'.join(sorted(articles)))
    return

if __name__ == "__main__":
    load_dump()
    find_articles()