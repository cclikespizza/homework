# coding=utf-8
__author__ = 'elmira'

import time
import re

reg = re.compile(u'\\w+', flags=re.U | re.DOTALL)


def read_words(fname):
    with open(fname, 'r', encoding='utf-8') as words:
        w = set(words.read().lower().strip().replace('\r\n', '\n').split('\n'))
    #     если убрать отсюда lower(), то станет чуточку быстрее (если считаем, что все слова в файле с маленькой буквы)
    #     если убрать set(), то станет еще чуточку быстрее (если считаем, что в файле слова не повторяются)
    return w


def read_poem(fname, words):
    # ---- preprocessing ----
    snippets, rhymes = p_split(fname)  # parse long_poem
    my_snippets = []
    my_rhymes = []
    # ---- preprocessing ----

    t1 = time.time()
    # ---- read and search ----
    w = read_words(words)
    for i in w:
        if i in snippets:
            my_snippets += snippets[i]
        if i in rhymes:
            my_rhymes += rhymes[i]
    # ---- read and search----
    t2 = time.time()

    with open('snippets.txt', 'w', encoding='utf-8') as sn, open('rhymes.txt', 'w', encoding='utf-8') as r:
        for i in my_rhymes:
            r.write(i+'\n')
        for i in my_snippets:
            sn.write(i+'\n')
    print(t2 - t1)


def p_split(fname):
    snippets = {}
    rhymes = {}
    last_words = []
    with open(fname, 'r', encoding='utf-8') as p:
        p2 = p.readlines()
        for n_line in range(len(p2)):
            # ---- create snippet ----
            res = ''
            if n_line != 0:
                res += p2[n_line - 1]
            res += p2[n_line]
            if n_line != len(p2) - 1:
                res += p2[n_line + 1]
            # ---- create snippet ----

            l2 = reg.findall(p2[n_line].lower())

            # ---- get rhyming words ----
            # think i'd better rewrite this piece
            if len(last_words) >= 2:
                for prev in [-1, -2]:
                    if l2[-1][-2:] == last_words[prev][-2:]:
                        # decided to be straightforward: similar words have same two last letters
                        if l2[-1] not in rhymes:
                            rhymes[l2[-1]] = {last_words[prev]}
                        else:
                            rhymes[l2[-1]].add(last_words[prev])
                        if last_words[prev] not in rhymes:
                            rhymes[last_words[prev]] = {l2[-1]}
                        else:
                            rhymes[last_words[prev]].add(l2[-1])
                last_words.append(l2[-1])
            else:
                if len(last_words) == 1:
                    if l2[-1][-2:] == last_words[-1][-2:]:
                        rhymes[l2[-1]] = {last_words[-1]}
                        rhymes[last_words[-1]] = {l2[-1]}
                    last_words.append(l2[-1])
                if len(last_words) == 0:
                    last_words.append(l2[-1])
            # ---- get rhyming words ----

            # ---- collect generated snippet for each word in line ----
            for i in l2:
                if i in snippets:
                    snippets[i].append(res)
                else:
                    snippets[i] = [res]
            # ---- ----------------------------------------------- ----
    return snippets, rhymes


if __name__ == "__main__":
    read_poem(u'long_poem.txt', u'words.txt')
