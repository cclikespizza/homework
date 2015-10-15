# encoding=utf-8
__author__ = 'elmira'

import re
import sqlite3 as sqlite
from html import unescape

regLinks = re.compile('\[\[.*?\]\]', flags=re.U | re.DOTALL)
regWords = re.compile(u'\\w+', flags=re.U | re.DOTALL)
regTags = re.compile(u'<[^>]*>', flags=re.U | re.DOTALL)
regURLs = re.compile(u'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', flags=re.U | re.DOTALL)


class Database(object):
    def __init__(self, db_file):
        self._connection = sqlite.connect(db_file)
        self._cursor = self._connection.cursor()

    def __exists(self, q):
        self._cursor.execute(q)
        s = self._cursor.fetchall()
        if len(s) <= 0:
            return False, None
        return True, s

    def table_exists(self, tname):
        table_search = 'SELECT name FROM sqlite_master WHERE type="table" AND name="' + tname + '";'
        return self.__exists(table_search)[0]

    def create_tables(self, tablename, *args):
        query = 'CREATE TABLE ' + tablename +' (' + ', '.join(args) + ');'
        self._cursor.execute(query)

    def insert(self, table, *args):
        data = [str(i) for i in args]
        q = "INSERT into " + table +" VALUES(" + ', '.join(['?']*len(args)) + u');'
        self._cursor.execute(q, data)

    def commit(self):
        self._connection.commit()

    def update(self, table, field1, value, field2, data):
        q = "UPDATE " + table +" SET " + field2 + '=' + str(value) + ' WHERE ' + field1 + '="' + data + '";'
        # print(q)
        self._cursor.execute(q)
        # self.commit()

    def increment(self, table, field, field2, data):
        q = 'SELECT '+field2 +' FROM '+ table +' WHERE ' + field + '="' + data + '";'
        exists, rows = self.__exists(q)
        if exists:
            self.update(table, field, rows[0][0]+1, field2, data)
        else:
            self.insert(table, data, 1)


def count_words(fname):
    print('start____count')
    commits = 0
    db = Database(u'db.dtb')
    if not db.table_exists('frequency1'):
        db.create_tables('frequency1', 'word TEXT', 'freq INTEGER')
    with open(fname, 'r', encoding='utf-8') as dump:
        flag = False
        flag2 = False
        for line in dump:
            s = line.lower().strip()
            if s.startswith('<title>') and s.endswith('</title>') and ':' not in s:
                print(regTags.sub('', s))
                flag2 = True
            if s.startswith('<text xml:space="preserve">') and flag2:
                flag = True
            if flag:
                s2 = unescape(regTags.sub('', s))
                s2 = regURLs.sub('',  s2)
                words = regWords.findall(s2)
                for i in words:
                    db.increment('frequency1', 'word', 'freq', i)
                    commits += 1
            if '</text>' in s and flag2:
                flag = False
                flag2 = False
            if commits >= 10000:
                db.commit()
                commits = 0
    db.commit()

# count_words('udmwiki-latest-pages-articles.xml')
