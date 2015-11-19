# coding=utf-8
__author__ = 'elmira'
import codecs
from collections import defaultdict


class Queue:

    def __init__(self, arr=None):
        if arr is None or not isinstance(arr, list):
            self.arr = []
        else:
            self.arr = arr

    def not_empty(self):
        if self.arr != []:
            return True
        return False

    def enqueue(self, element):
        self.arr.append(element)

    def dequeue(self):
        if self.not_empty():
            x = self.arr[0]
            del self.arr[0]
            return x

    def str(self):
        return self.arr


class Keyboard:
    # keyboard rows and columns (both english and russian)
    arrs = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm',
            # !! uncomment these lines to take into account all close letters from other rows !!
            # 'qaz', 'wsx', 'edc', 'rfv', 'tgb', 'yhn', 'ujm', 'ik', 'ol',
            # 'wa', 'esz', 'rdx', 'tfc', 'ygv', 'uhb', 'ijn', 'okm', 'pl',
            'йцукенгшщзхъ', 'фывапролджэ', 'ячсмитьбю',
            # 'йфя', 'цыч', 'увс', 'кам', 'епи', 'нрт', 'гоь', 'шлб', 'щдю', 'зж', 'хэ',
            # 'цф', 'уыя', 'квч', 'еас', 'нпм', 'гри', 'шот', 'щль', 'здб', 'хжю', 'ъэ'
            ]

    def __init__(self):
        # Creates a dictionary {letter: string of close letters}, e.g. {'j': 'hkumin', 'ч': 'ясыв'}
        self.dict = defaultdict(str)
        for word in self.arrs:
            for ln in zip(word, word[1:]):
                self.dict[ln[0]] += ln[1]
                self.dict[ln[1]] += ln[0]

    def close(self, a, b):
        # checks whether letters a and b are close on keyboard
        if b in self.dict[a] or a in self.dict[b]:
            return True
        return False


class Spellchecker:

    def __init__(self, fname=None):
        if fname is None:
            self.words = self.open_words('words.txt')
        else:
            self.words = self.open_words(fname)

    def levenshtein(self, word1, word2, insert=1, delete=1, sub_close=0.5, sub_dist=1):
        table = [[j for j in range(len(word1) + 1)]] +\
                [[i + 1] + [None] * len(word1)
                 for i in range(len(word2))]

        on_keyboard = Keyboard()

        for i in range(len(word2)):
            for j in range(len(word1)):
                if word1[j] == word2[i]:
                    replacement = table[i][j]
                elif on_keyboard.close(word1[j], word2[i]):
                    replacement = table[i][j] + sub_close
                else:
                    replacement = table[i][j] + sub_dist
                insertion = table[i][j + 1] + insert
                removal = table[i + 1][j] + delete
                table[i + 1][j + 1] = min(replacement,
                                          insertion, removal)
        return table[len(word2)][len(word1)]

    def open_words(self, fname):
        with codecs.open(fname, 'r', encoding='utf-8') as book:
            r = book.readlines()
            r = set([word.strip('\r\n').lower() for word in r])
        return r

    def check(self, word):
        d = defaultdict(list)
        for entry in self.words:
            # if the list of words is long, this takes quite a lot of time!
            d[self.levenshtein(word, entry)].append(entry)
        sorted_hits = Queue(sorted(d.keys()))
        best_hit = d[sorted_hits.dequeue()]
        if len(best_hit) < 3:
            while len(best_hit) < 3 and sorted_hits.not_empty():
                best_hit += d[sorted_hits.dequeue()]
        return ', '.join(best_hit[:3])


if __name__ == "__main__":
    sp = Spellchecker('words.txt')
    user_word = input("Введите слово: ")
    while user_word != '':
        print(sp.check(user_word))
        user_word = input("Введите слово: ")
