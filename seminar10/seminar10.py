__author__ = 'elmira'
from lxml import etree
from collections import Counter
from itertools import product
import os
from math import log

# + Возьмите небольшой корпус, состоящий из достаточно большого числа документов.
# + Лемматизируйте его.

# Я скачала несколько статей из русской википедии, прогнала их через майстем и собрала все в папке /xml


def open_text(fname):
    # Открываем текст и делаем из него список лемм
    parser = etree.HTMLParser()
    tree = etree.parse(fname, parser).getroot()[0]
    words = [w[0].attrib['lex'] for se in tree for w in se if len(w) != 0]  # массив лемм всего текста
    return fname, words


def collect_corpus(directory='xml'):
    # Создаем набор тектсов, где каждый текст - это список лемм.
    texts = [open_text(directory + '/' + fname) for fname in os.listdir(directory)]
    return texts


def unique(texts):
    # Составляем множество уникальных лемм всего корпуса.
    unique_lems = set()
    for text in texts:
        unique_lems.update(text[1])
    return unique_lems


def create_idf_dict(lems, texts):
    # Составляем словарь idf, в котором для каждой леммы хранится log(N/df),
    # где N – число документов, df – число документов, содержащих данную лемму.
    N = len(texts)
    dic = {lem: log(N/sum([lem in text[1] for text in texts])) for lem in lems}
    return dic


def create_tfidf_dict(lems, texts, idf):
    texts = {i[0]: Counter(i[1]) for i in texts}
    dic = {}
    for i in product(lems, texts.keys()):
        dic[i] = (texts[i[1]][i[0]]/len(texts[i[1]]))*idf[i[0]]
    return dic


def main():
    print('Собираю тексты корпуса...')
    corpus = collect_corpus()
    print('Собираю список уникальных лемм...')
    uniq = unique(corpus)
    print('Считаю idf...')
    idf = create_idf_dict(uniq, corpus)
    print('Считаю tf-idf...')
    tfidf = create_tfidf_dict(uniq, corpus, idf)
    print('Пары лемма-документ с наибольшим значением tf-idf:')
    for pair in sorted(tfidf, key=lambda x:tfidf[x], reverse=True)[:10]:
        print('   ' + pair[0] + ' - ' + pair[1])

if __name__ == "__main__":
    main()