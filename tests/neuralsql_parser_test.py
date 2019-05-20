from neuralsql_parser import parse
import unittest


class TestNeuralSQLParser(unittest.TestCase):
    def test_wordcount(self):
        sql = "SELECT content FROM text8.train TRAINER WordCount;"
        parse(sql)

        sql = "SELECT content FROM text8.train TRAINER WordCount INTO wordcount;"
        parse(sql)

    def test_word2vec(self):
        sql = "SELECT data FROM word2vec.corpus TRAINER word2vec;"
        parse(sql)

    def test_classifier(self):
        sql = "SELECT content FROM Sys.dual TRAINER classifier.SGDClassifier WITH loss='hinge', penalty='l2', random_state=42, max_iter=5, tol=None;"
        parse(sql)

        # TODO scientific notation
        # sql = "SELECT content FROM Sys.dual TRAINER classifier.SGDClassifier WITH loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None;"
        # parse(sql)

        sql = "SELECT content FROM twenty_news.train TRAINER classifier.MultinomialNB;"
        parse(sql)

    def test_clustering(self):
        sql = "SELECT content FROM twenty_news.train TRAINER clustering.KMeans;"
        parse(sql)

    def test_chatbot(self):
        pass


if __name__ == '__main__':
    unittest.main()
