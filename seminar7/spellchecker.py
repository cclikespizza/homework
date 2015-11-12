# coding=utf-8
__author__ = 'elmira'
import codecs
from collections import Counter, defaultdict
import re

class Keyboard:
    arrs = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm', 'qaz', 'wsx', 'edc', 'rfv', 'tgb', 'yhn', 'ujm', 'ik', 'ol']

    def __init__(self):
        self.dict = defaultdict(str)
        for word in self.arrs:
            for ln in range(1, len(word)):
                self.dict[word[ln]] += word[ln-1]
                self.dict[word[ln-1]] += word[ln]

    def close(self, a, b):
        if b in self.dict[a] or a in self.dict[b]:
            return True
        return False


class Spellchecker:

    def __init__(self, fname=None):
        if fname is None:
            self.dic = self.open_book('book1.txt')
        else:
            self.dic = self.open_book(fname)

    def levenshtein(self, word1, word2, insert=1, delete=1, sub_close=1, sub_dist=2):
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

    def open_book(self, fname):
        with codecs.open(fname, 'r', 'utf-8') as book:
            r = book.readlines()
            r = [word.strip('\r\n').lower() for word in r]
            dict = Counter(r)
        return dict

    def check(self, word):
        if word in self.dic:
            return word
        d = defaultdict(list)
        for key in self.dic:
            d[self.levenshtein(word, key)].append(key)
        bestDif = d[sorted(d.keys())[0]]
        res = sorted([(w, self.dic[w]) for w in bestDif], key=lambda a: a[1], reverse=True)
        return res

    def check_word(self, word):
        res = self.check(word)
        if isinstance(res, list):
            return ', '.join(i[0] for i in res)
        return res

    def check_text(self, text):
        result = ''
        text = re.split(u'([ .,()–‒―—;!%$‱‰·»:<?>«*-\\[\\]^|{}+;\r\n])', text)
        for i in text:
            if i in u' .,()–‒―—;!%$‱‰·»:<?>«*-\\[\\]^|{}+;\r\n':
                result += i
            else:
                temp = self.check(i.lower())
                if isinstance(temp, list):
                    if i[0].isupper():
                        result += temp[0][0][0].upper() + temp[0][0][1:]
                    else:
                        result += temp[0][0]
                else:
                    if i[0].isupper():
                        result += temp[0].upper() + temp[1:]
                    else:
                        result += temp
        return result


sp = Spellchecker()
# check_word -
# если нужно слово заменить, перечисляет все варианты замены и сколько раз они встретились в тексте,
# а если не нужно заменять, просто возвращает само слово
# print(sp.check_word(u'dsgvser'))
# print(sp.check_word(u'apple'))
# print(sp.check_word(u'qwertyuiop'))
print(sp.check_word(u'qwerty'))
