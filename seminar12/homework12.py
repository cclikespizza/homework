__author__ = 'elmira'

from pymystem3 import Mystem
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from scipy import sparse
import numpy as np
from sklearn import svm, naive_bayes, grid_search

morph = Mystem()
POS = ['A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 'COM', 'CONJ', 'INTJ', 'NUM', 'PART', 'PR', 'S', 'SPRO', 'V']


def open_news(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        texts = f.read().split('\n\n')  # каждая новость отделена двумя переносами строки
        arr = [news.strip() for news in texts if news != '']
        # возвращаем массив новостей
    return arr


def count_pos(arr):
    analysis = [morph.analyze(news) for news in arr]
    pos = [Counter([dic['analysis'][0]['gr'].split('=')[0].split(',')[0] for dic in i if 'analysis' in dic and len(dic['analysis']) > 0]) for i in analysis]
    return pos


def count_tfidf(texts):
    cv = CountVectorizer()
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(cv.fit_transform(texts))
    return X_train_tfidf


def main():
    print('Читаю тексты...')
    # pymystem3 вообще какой-то долгий =(
    # поэтому я тестила на politics2.txt & culture2.txt
    politics = open_news('politics.txt')
    culture = open_news('culture.txt')

    print('Считаю число вхождений частей речи...')
    pos1 = count_pos(politics)
    pos2 = count_pos(culture)

    print('Создаю таблицы...')
    politics_pos = np.array([[d[i] for i in POS] for d in pos1])
    culture_pos = np.array([[d[i] for i in POS] for d in pos2])
    pos_data = np.vstack((politics_pos, culture_pos))
    tfidf_data = count_tfidf(politics + culture)
    features = sparse.hstack((pos_data, tfidf_data))
    target = np.array([0]*len(pos1) + [1]*len(pos2))

    print('Учимся...')
    parameters = {'C': (.005, .1, .5, 1.0)}
    gs1 = grid_search.GridSearchCV(svm.SVC(), parameters)
    gs1.fit(features, target)
    print('Процент успеха SVC:', gs1.best_score_)
    parameters = {'alpha': (1.0, 1e-3)}
    gs2 = grid_search.GridSearchCV(naive_bayes.MultinomialNB(), parameters)
    gs2.fit(features, target)
    print('Процент успеха MultinomialNB:', gs2.best_score_)
    print()

    best = gs1.best_estimator_ if gs1.best_score_ > gs2.best_score_ else gs2.best_estimator_

    example_true = []
    example_false = []
    f = features.toarray()
    for i in range(len(politics)):
        guess = best.predict(f[i].reshape(1, -1))
        if guess != 0:
            if len(example_false) < 3:
                example_false.append(politics[i])
        else:
            if len(example_true) < 3:
                example_true.append(politics[i])
        if len(example_false) >= 3 and len(example_true) >= 3:
            break
    for i in range(len(culture)):
        guess = best.predict(f[i+len(politics)].reshape(1, -1))
        if guess != 0:
            if len(example_false) < 3:
                example_false.append(culture[i])
        else:
            if len(example_true) < 3:
                example_true.append(culture[i])
        if len(example_false) >= 3 and len(example_true) >= 3:
            break

    print('Примеры, где машина ошибается: ')
    for i in example_false:
        print('   ', i)
    print('Примеры, где машина угадывает: ')
    for i in example_true:
        print('   ', i)

if __name__ == "__main__":
    main()