__author__ = 'elmira'

import numpy as np
import itertools
from matplotlib import mlab
import re

with open('corpus1.txt', encoding='utf-8') as f:
    news = f.read()
with open('corpus2.txt', encoding='utf-8') as f:
    anna = f.read()

anna_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', anna)
news_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', news)


def words(sentence):
    return sentence.lower().split()

def word_lens(sentence):
    return [len(i) for i in sentence]

def different_letters(sentence):
    russian_letters = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
    # число различных букв в предложении,
    letters = set()
    for word in sentence:
        for letter in word:
            if letter in russian_letters:
                letters.add(letter)
    return len(letters)

def vowels(word):
    vowel_arr = 'ёуеэоаыяию'
    num = 0
    for letter in word:
        if letter in vowel_arr:
            num += 1
    return num

def vowels_in_sent(sentence):
    # число гласных в предложении,
    return [vowels(word) for word in sentence]

anna_sent = [words(sentence) for sentence in anna_sentences if len(words(sentence)) > 0]
news_sent = [words(sentence) for sentence in news_sentences if len(words(sentence)) > 0]

anna_data = [(sum(word_lens(sentence)),  # длина предложения в буквах,
              different_letters(sentence),  # число различных букв в предложении,
              sum(vowels_in_sent(sentence)),  # число гласных в предложении,
              np.median(word_lens(sentence)),  # медиана числа букв в слове,
              np.median(vowels_in_sent(sentence)))  # медиана числа гласных в слове.
             for sentence in anna_sent]

news_data = [(sum(word_lens(sentence)),
              different_letters(sentence),
              sum(vowels_in_sent(sentence)),
              np.median(word_lens(sentence)),
              np.median(vowels_in_sent(sentence)))
             for sentence in news_sent]

from matplotlib import pyplot as plt
anna_data = np.array(anna_data)
news_data = np.array(news_data)

# ВОТ ДЗ:

data = np.vstack((anna_data, news_data))
p = mlab.PCA(data, True)
N = len(anna_data)

plt.plot(p.Y[:N,0], p.Y[:N,1], 'og', p.Y[N:,0], p.Y[N:,1], 'sb')
plt.show()
print(p.Wt)