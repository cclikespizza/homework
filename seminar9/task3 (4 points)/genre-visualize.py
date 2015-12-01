__author__ = 'elmira'

import numpy as np
from lxml import etree
from collections import Counter
from matplotlib import pyplot as plt
from matplotlib import mlab
import itertools


class Text:
    features = ['длина предложения в словах', 'длина предложения в буквах',
                'число различных букв в предложении', 'число гласных в предложении',
                'медиана числа букв в слове (медианная длина)', 'среднее число букв в слове (средняя длина слова)',
                'медиана числа гласных в слове', 'количество прилагательных',
                'количество существительных', 'количество глаголов',
                'количество наречий', 'количество местоимений']

    def __init__(self, fname):
        self.sentences = self.open_corpus(fname)

    @staticmethod
    def open_corpus(fname):
        parser = etree.HTMLParser()
        tree = etree.parse(fname, parser).getroot()[0]
        return tree

    def make_features(self):
        sentences = [self.sent_words(sent) for sent in self.sentences]  # каждое предложение -- массив слов
        data = [[len(sentence),  # длина предложения в словах,
                 sum(self.word_lens(sentence)),  # длина предложения в буквах,
                 self.different_letters(sentence),  # число различных букв в предложении,
                 sum(self.vowels_in_sent(sentence)),  # число гласных в предложении,
                 np.median(self.word_lens(sentence)),  # медиана числа букв в слове (медианная длина),
                 np.mean(self.word_lens(sentence)),  # среднее число букв в слове (средняя длина слова),
                 np.median(self.vowels_in_sent(sentence))]  # медиана числа гласных в слове.
                for sentence in sentences]
        pos_data = [self.pos_features(sent) for sent in self.sentences]  # массив про части речи

        return np.array([i+y for i,y in zip(data, pos_data)])

    @staticmethod
    def pos_features(sent):
        d = Counter([w[0].attrib['gr'].split('=')[0].split(',')[0] for w in sent if len(w) != 0])
        return [d['A'], d['S'], d['V'], d['ADV'], d['SPRO'] + d['APRO'] + d['ADVPRO']]

    @staticmethod
    def sent_words(sent):
        arr = [w.text.lower() for w in sent]
        return arr

    @staticmethod
    def word_lens(sentence):
        return [len(i) for i in sentence]

    @staticmethod
    def different_letters(sentence):
        russian_letters = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
        # число различных букв в предложении,
        letters = set()
        for word in sentence:
            for letter in word:
                if letter in russian_letters:
                    letters.add(letter)
        return len(letters)

    @staticmethod
    def vowels(word):
        vowel_arr = 'ёуеэоаыяию'
        num = 0
        for letter in word:
            if letter in vowel_arr:
                num += 1
        return num

    def vowels_in_sent(self, sentence):
        # число гласных в предложении,
        return [self.vowels(word) for word in sentence]


def main():
    print('Читаю тексты...')
    sonets = Text('corpus1.txt')
    anna = Text('corpus2.txt')
    news = Text('corpus3.txt')

    print('Считаю характеристики...')
    sonets_data = sonets.make_features()
    anna_data = anna.make_features()
    news_data = news.make_features()

    print('Использую метод главных компонент...')
    data = np.vstack((sonets_data, anna_data, news_data))
    p = mlab.PCA(data, True)
    N1 = len(sonets_data)
    N2 = len(anna_data)

    print('Значимые признаки:')
    main_features = sorted(zip(Text.features, p.s, range(12)), key=lambda pair: -abs(pair[1]))[:3]
    print('\r\n'.join('   ' + par[0] + ' - ' + str(par[1]) for par in main_features))

    print('Рисую графики...')
    plt.figure()
    plt.plot(p.Y[:N1,0], p.Y[:N1,1], 'og', p.Y[N1:N2+N1,0], p.Y[N1:N2+N1,1], 'sb', p.Y[N2+N1:,0], p.Y[N2+N1:,1], 'xr')
    plt.savefig('PCA-result.png')
    plt.close()

    for i, j in itertools.combinations(main_features, 2):
        plt.figure()
        plt.plot(data[:N1,i[2]], data[:N1,j[2]], 'og', data[N1:N2+N1,i[2]], data[N1:N2+N1,j[2]], 'sb', data[N2+N1:,j[2]], data[N2+N1:,j[2]], 'xr')
        plt.savefig('%s_vs_%s.png' % (Text.features[i[2]], Text.features[j[2]]))
        plt.close()

    print('Ура! Конец!')


if __name__ == "__main__":
    main()