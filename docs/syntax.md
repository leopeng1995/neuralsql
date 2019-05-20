## NeuralSQL Syntax


```
SELECT content FROM <database_name>.<table_name> TRAINER WordCount;
```

```
SELECT content FROM <database_name>.<table_name> TRAINER TFIDF;
```

```
SELECT content FROM <database_name>.<table_name> TRAINER clustering.KMeans;
```

```
SELECT content FROM <database_name>.<table_name> TRAINER classifier.MultinomialNB;
```

```
SELECT content FROM <database_name>.<table_name> TRAINER classifier.SGDClassifier WITH loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None;
```

文本 Word2Vec

```
SELECT data FROM word2vec.corpus TRAINER word2vec;

```

文本情绪分析

```
SELECT data FROM amazon.comments TRAINER sentiment_analysis;
```

```
SELECT data FROM text8.train TRAINER chatbot;
```
