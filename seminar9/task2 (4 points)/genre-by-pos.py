__author__ = 'elmira'

import numpy as np
from lxml import etree
from collections import Counter
from matplotlib import pyplot as plt
from matplotlib import mlab


def open_corpus(fname):
    parser = etree.HTMLParser()  # создаем парсер хтмл-страниц
    # скармливаем парсеру xml, берем тэг body и все что внутри него
    tree = etree.parse(fname, parser).getroot()[0]
    sents = [Counter([w[0].attrib['gr'].split('=')[0].split(',')[0] for w in se if len(w) != 0]) for se in tree]
    # этот дико жуткий list comprehension делает из каждого предложения массив
    # в этом массиве находятся подряд части речи входящих в предложение слов
    # # если у слова есть омонимия, то берется самый первый разбор
    # # если майстем слово не разобрал, то слово игнорируется
    # а потом каждый массив превращается в словарь, в котором написано, сколько раз какая часть речи встретилась
    return sents


def make_features(data):
    return np.array([(d['A'],
             d['S'],
             d['V'],
             d['ADV'],
             d['SPRO'] + d['APRO'] + d['ADVPRO'])  # за местоимения считаются и мест-сущ, и мест-прил, и мест-наречие
            for d in data])


def main():
    sonets = open_corpus('corpus1.txt')
    anna = open_corpus('corpus2.txt')

    sonets_data = make_features(sonets)
    anna_data = make_features(anna)

    data = np.vstack((sonets_data, anna_data))
    p = mlab.PCA(data, True)
    N = len(sonets_data)
    print(p.Wt)

    plt.plot(p.Y[N:,0], p.Y[N:,1], 'og', p.Y[:N,0], p.Y[:N,1], 'sb')
    # зелененькое - анна каренина, а синенькое - сонеты

    # Правда ли, что существует линейная комбинация признаков (т.е. значение по первой оси в преобразованных методом главных компонент данных), и пороговое значение, при которых больше 70% текстов каждого жанра находятся с одной стороны от порогового значения? Напишите программу genre-by-pos.py, которая демонстрирует ответ на этот вопрос.

    # Мне кажется, что ответ да, судя по картинке
    plt.show()
    # Подберем, например, на глаз по картинке пороговое значение,
    # при котором больше 70% предложений анны карениной справа от него, и больше 70% предложений сонетов -- слева
    # Например, -4.2 :
    print(sum(p.Y[N:,0]>-4.2)/len(p.Y[N:,0]))
    print(sum(p.Y[:N,0]<-4.2)/len(p.Y[:N,0]))


if __name__ == "__main__":
    main()