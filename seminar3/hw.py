# encoding=utf-8
__author__ = 'elmira'

import re
from html import unescape

regLinks = re.compile('\[\[.*?\]\]', flags=re.U | re.DOTALL)
regWords = re.compile(u'\\w+', flags=re.U | re.DOTALL)
regTags = re.compile(u'<[^>]*>', flags=re.U | re.DOTALL)


class Article(object):
    def __init__(self, name):
        self.name = name
        self.words = 0
        self.links = 0

    def __str__(self):
        return ','.join([self.name, str(self.links), str(self.words)])


def find_articles(fname):
    """
    Prints to file the names of all articles from Wikipedia for a specified language.
    """
    articles = []
    with open(fname, 'r', encoding='utf-8') as dump:
        flag = False
        for line in dump:
            s = line.strip()
            if s.startswith('<title>') and s.endswith('</title>'):
                article = Article(unescape(s.replace('<title>', '').replace('</title>', '')))
            if s.startswith('<text xml:space="preserve">'):
                flag = True
            if flag:
                words = regWords.findall(s)
                links = regLinks.findall(s)
                article.links += len(links)
                article.words += len(words)
            if '</text>' in s:
                flag = False
                articles.append(str(article))
    open('article_names.txt', 'w', encoding='utf-8').write('\n'.join(articles))
    return

find_articles('udmwiki-latest-pages-articles.xml')