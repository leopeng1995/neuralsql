from pprint import pprint

import pymongo
from pyparsing import ParseException

from neuralsql.operator.wordcount import generate_mapper
from neuralsql.operator.wordcount import generate_reducer
from neuralsql_parser import parse

from neuralsql.sql.load_samples import *
from neuralsql.operator.classifiers import *


class SQLExecutor(object):
    def __init__(self, host, port):
        self.host = host or 'localhost'
        self.port = port or 27017
        self.client = None
        self.connect()

    def connect(self):
        self.client = pymongo.MongoClient(self.host, self.port)

    def server_type(self):
        return self.client.server_info()['version']

    def run(self, statement):
        try:
            parsed_result = parse(statement)
            database = parsed_result['database']
            table = parsed_result['table']

            # TODO fetch data first

            if parsed_result['trainable']:
                trainer = parsed_result['trainer'].lower()
                results = list()
                if trainer == 'wordcount':
                    results = self.client[database][table].map_reduce(generate_mapper('content'), generate_reducer(),
                                                                      "wordcount")
                    for doc in results.find():
                        pprint(doc)
                elif trainer.startswith('classifier.'):
                    if trainer.endswith('multinomialnb'):
                        generate_MultinomialNB()
                    elif trainer.endswith('sgdclassifier'):
                        generate_SGDClassifier()
                elif trainer == 'chatbot':
                    pass
                elif trainer == 'word2vec':
                    pass
            else:
                for doc in self.client[database][table].find():
                    pprint(doc)
        except ParseException as e:
            print(e.msg)

    def load_sample(self, sample):
        if sample.startswith('wordcount'):
            if sample == 'wordcount' or sample == 'wordcount[english]':
                load_wordcount_english_dataset_into_mongodb(self.client)
            elif sample == 'wordcount[chinese]':
                load_wordcount_chinese_dataset_into_mongodb(self.client)
        elif sample.startswith('word2vec'):
            if sample == 'word2vec' or sample == 'word2vec[english]':
                pass
            elif sample == 'word2vec[chinese]':
                pass
        elif sample.startswith('chatbot'):
            if sample == 'chatbot' or sample == 'chatbot[english]':
                pass
            elif sample == 'chatbot[chinese]':
                pass
        elif sample.startswith('classifier'):
            if sample == 'classifier' or sample == 'classifier[twenty_news]':
                load_classifier_twenty_news_dataset_into_mongodb(self.client)
            elif sample == 'classifier[iris]':
                pass
