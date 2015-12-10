__author__ = 'elmira'
from lxml import etree
from collections import Counter
import numpy as np
from sklearn import svm, grid_search

POS = ['A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 'COM', 'CONJ', 'INTJ', 'NUM', 'PART', 'PR', 'S', 'SPRO', 'V']


def open_corpus(fname):
    parser = etree.HTMLParser()
    tree = etree.parse(fname, parser).getroot()[0]
    sents = [' '.join([w.text + w.tail.strip() for w in se]) for se in tree]  # сами предложения
    pos_counts = [Counter([w[0].attrib['gr'].split('=')[0].split(',')[0] for w in se if len(w) != 0]) for se in tree]
    #  массив, где для каждого предложения - число вхождений каждой части речи
    return sents, pos_counts


def main():
    print('Читаю тексты...')
    kapital_sents, kapital_pos = open_corpus('kapital.xml')
    voina_sents, voina_pos = open_corpus('voina.xml')

    print('Создаю таблицы...')
    kapital_table = np.array([[d[i] for i in POS] for d in kapital_pos])
    voina_table = np.array([[d[i] for i in POS] for d in voina_pos])
    data = np.vstack((kapital_table, voina_table))
    target = np.array([0 for _ in kapital_pos] + [1 for _ in voina_pos])

    print('Учимся...')
    parameters = {'C': (.005, .1, .5, 1.0)}
    gs = grid_search.GridSearchCV(svm.LinearSVC(), parameters)
    gs.fit(data, target)
    print()

    print('Процент успеха:', gs.best_score_)
    best = gs.best_estimator_

    example_true = []
    example_false = []
    for i in range(len(kapital_table)):
        guess = best.predict(kapital_table[i].reshape(1, -1))
        if guess != 0:
            if len(example_false) < 3:
                example_false.append((kapital_sents[i], kapital_table[i]))
        else:
            if len(example_true) < 3:
                example_true.append((kapital_sents[i], kapital_table[i]))
        if len(example_false) >= 3 and len(example_true) >= 3:
            break

    print('Примеры, где машина ошибается: ')
    for i in example_false:
        print('   ', i[0], i[1])
    print('Примеры, где машина угадывает: ')
    for i in example_true:
        print('   ', i[0], i[1])

if __name__ == "__main__":
    main()