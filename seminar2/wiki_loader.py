# encoding=utf-8
__author__ = 'elmira'

import urllib.request as urlr
from urllib.error import HTTPError
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
    # todo
    # Вторая функция тоже должна спрашивать у пользователя код языка,
    # после чего она должна открыть предварительно загруженный и (вручную)
    # разархивированный xml-файл с дампом и вывести в новый файл article_names.txt
    # список названий всех статей из этого языкового раздела википедии в алфавитном порядке.
    # Программа должна корректно работать даже в том случае, когда дамп имеет
    # огромный размер, превышающий размер оперативной памяти компьютера.
    pass
    code = input('Input language code: ')  # ru, en, udm
    with open(code + 'wiki-latest-pages-articles.xml', 'r', encoding='utf-8') as dump:
        pass
