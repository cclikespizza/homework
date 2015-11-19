__author__ = 'elmira'

import numpy as np
import itertools
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

# построила графики для всех комбинаций наших признаков:
# for i, j in itertools.combinations([0,1,2,3,4], 2):
#     print(i,j)
#     plt.figure()
#     plt.plot(anna_data[:,i], anna_data[:,j], 'sb',
#              news_data[:,i], news_data[:,j], 'og')
#     plt.show()

plt.figure()
plt.plot(anna_data[:,2], anna_data[:,3], 'sb',
         news_data[:,2], news_data[:,3], 'og')
plt.show()
# лучше всего разделение получилось по осям 2 и 3 - число гласных в предложении, медиана числа букв в слове