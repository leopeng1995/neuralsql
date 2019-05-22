import os
import math
import requests
import zipfile
import codecs

from tqdm import tqdm
from sklearn.datasets import fetch_20newsgroups

data_dir = os.path.expanduser('~/neuralsql_data')

if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def download_file(url, path):
    r = requests.get(url, stream=True)

    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    with open(path, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size // block_size), unit='KB',
                         unit_scale=True):
            wrote = wrote + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")


# TODO avoid inserting data repeatedly
def load_wordcount_english_dataset_into_mongodb(client, database='text8', table='train', words_per_document=1000):
    # Download a small chunk of Wikipedia articles collection
    url = 'http://mattmahoney.net/dc/text8.zip'
    path = os.path.join(data_dir, 'text8.zip')
    if not os.path.exists(path):
        print("Downloading the dataset... (It may take some time)")
        download_file(url, path)

    # Unzip the dataset file. Text has already been processed
    with zipfile.ZipFile(path) as f:
        f.extractall(data_dir)

    path = os.path.join(data_dir, 'text8')
    with codecs.open(path, 'r', 'utf8') as fp:
        lines = fp.readlines()

    line = lines[0]
    words = line.split()

    cur = 0
    sentences = list()
    while cur * words_per_document < len(words):
        left = cur * words_per_document
        right = (cur + 1) * words_per_document
        sentences.append(words[left:right])
        cur = cur + 1

    data_list = list()
    db = client[database]
    for i, sentence in enumerate(sentences):
        data = dict()
        content = ' '.join(sentence)
        data['content'] = content
        data_list.append(data)

        if i % 100 == 0:
            db[table].insert_many(data_list)
            data_list = list()

        # db[table].insert_one(data)
        # data_list.append(data)

    print('WordCount Data Prepared.')


def load_wordcount_chinese_dataset_into_mongodb(client):
    pass


def load_classifier_twenty_news_dataset_into_mongodb(client, database='twenty_news'):
    twenty_train = fetch_20newsgroups(subset='train')
    twenty_test = fetch_20newsgroups(subset='test')

    db = client[database]

    data_list = list()
    for i, datum in enumerate(twenty_train.data):
        filename = twenty_train.filenames[i].split('/')[-1]

        if not db.train.find_one({'id': filename}):
            data = dict()
            data['id'] = filename
            data['data'] = datum
            # TODO use mongodb way to generate this field
            data['target'] = twenty_train.target[i].item()

            target = twenty_train.target[i]
            target_name = twenty_train.target_names[target]

            data_list.append(data)

    if data_list:
        db.train.insert_many(data_list)

    data_list = list()
    for i, datum in enumerate(twenty_test.data):
        filename = twenty_test.filenames[i].split('/')[-1]

        if not db.test.find_one({'id': filename}):
            data = dict()
            data['id'] = filename
            data['data'] = datum
            # TODO use mongodb way to generate this field
            data['target'] = twenty_train.target[i].item()

            target = twenty_test.target[i]
            target_name = twenty_test.target_names[target]

            data_list.append(data)

    if data_list:
        db.test.insert_many(data_list)

    print('Classifier Data Prepared.')
