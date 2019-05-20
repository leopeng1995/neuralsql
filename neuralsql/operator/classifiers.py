import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

categories = ['alt.atheism', 'soc.religion.christian',
              'comp.graphics', 'sci.med']

# twenty_train = fetch_20newsgroups(subset='train')
twenty_train = fetch_20newsgroups(subset='train',
                                  categories=categories, shuffle=True, random_state=42)


def generate_MultinomialNB():
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])

    text_clf.fit(twenty_train.data, twenty_train.target)

    # twenty_test = fetch_20newsgroups(subset='test')
    twenty_test = fetch_20newsgroups(subset='test',
                                     categories=categories, shuffle=True, random_state=42)
    docs_test = twenty_test.data
    predicted = text_clf.predict(docs_test)
    print('Test data accuracy:', np.mean(predicted == twenty_test.target))


def generate_SGDClassifier():
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', SGDClassifier(loss='hinge', penalty='l2',
                              alpha=1e-3, random_state=42,
                              max_iter=5, tol=None)),
    ])

    text_clf.fit(twenty_train.data, twenty_train.target)

    # twenty_test = fetch_20newsgroups(subset='test')
    twenty_test = fetch_20newsgroups(subset='test',
                                     categories=categories, shuffle=True, random_state=42)
    docs_test = twenty_test.data
    predicted = text_clf.predict(docs_test)
    print('Test data accuracy:', np.mean(predicted == twenty_test.target))
