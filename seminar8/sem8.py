# coding=utf-8
__author__ = 'elmira'

import numpy as np

a = np.array([1,2,3])
print (a + np.array([1,-1, 0]))
# shape



# срезы, шаг

a = np.array([[1,2,3], [4, 0.7, -1]])
print (a)

print(a[0:2, 0:3:2])
print(np.zeros((4, 4, 4)))
print(np.ones((2, 3)))
print(np.ones((2, 3)) * 5)

x = np.array([5,9,8,13,16])
m = x.mean()
print(m)
print(x**2 - m**2)
sd = (x**2 - m**2).mean()**0.5
print(sd)
print(x.std())

with open('anna.txt', encoding='utf-8') as f:
    anna = f.read()

with open('sonets.txt', encoding='utf-8') as f:
    sonets = f.read()
import re
anna_sents = re.split(r'(:?[.]\s*){3}|[.!?]', anna)
sonet_sents = re.split(r'(:?[.]\s*){3}|[.!?]', sonets)


def words(sent):
    return [len(word) for word in sent.split()]

anna_sent_lens = [words(sent) for sent in anna_sents if len(words(sent)) > 0]
sonet_sent_lens = [words(sent) for sent in sonet_sents if len(words(sent)) > 0]

anna_data = np.array([len(sent), np.mean(sent), np.median(sent), np.std(sent)] for sent in anna_sent_lens)
sonet_data = np.array([len(sent), np.mean(sent), np.median(sent), np.std(sent)] for sent in sonet_sent_lens)

from matplotlib import pyplot as plt

plt.figure()
plt.plot(anna_data[:, 0], anna_data[:,1], 'o')
plt.show()