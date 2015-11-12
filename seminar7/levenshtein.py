__author__ = 'elmira'
from collections import defaultdict
# Расстояние Левенштейна
# w1, w2  D,I,E


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


def levenshtein(word1, word2, insertion=1, deletion=1, sub_close=1, sub_dist=1):
    # create a matrix
    m = []
    for letter in range(len(word1) + 1):
        s = [0] * (len(word2) + 1)
        m.append(s)
    for x in range(len(word2) + 1):
        m[0][x] = x
    for x in range(len(word1) + 1):
        m[x][0] = x
    # here we got a matrix m

    on_keyboard = Keyboard()

    # now count minimum edit distance
    for row in range(1, len(m[0])):
        for column in range(1, len(m)):
            if_deleted = m[column-1][row] + deletion
            if_inserted = m[column][row-1] + insertion
            if word2[row - 1] == word1[column - 1]:
                ps = 0
            elif on_keyboard.close(word2[row - 1], word1[column - 1]):
                ps = sub_close
            else:
                ps = sub_dist
            if_substituted = m[column-1][row-1] + ps
            m[column][row] = min(if_deleted, if_inserted, if_substituted)
    # in case you want to print out the matrix:
    #    for ar in reversed(m):
    #        print(ar)
    #    print()
    print('Minimum edit distance is ', m[len(word1)][len(word2)])

word1 = input(u'Input word one: ')
word2 = input(u'Input word two: ')
print()
levenshtein(word1, word2)
