## NeuralSQL - Make MongoDB More Intelligent

2019 MongoDB Hackathon Project

### What is NeuralSQL?

It is a simple query engine using SQL-like syntax. Only supported Python 3.x.

### Motivation

SQL is an intuitive way to query data. Nowadays, more and more data use MongoDB as their storage databases which are benefited by MongoDB NoSQL Features. We want to build a SQL-like query engine to train machine learning or deep learning models using data in the MongoDB. This experimental project also demonstrates my idea on serverless function to predict using pretrained model stored in MongoDB.

### Features

* Use SQL-like syntax to query MongoDB and get data insight.
* Used multiple backends, such as TensorFlow, Keras, or scikit-learn.
* Computation Engine for generates MongoDB pipeline/map-reduce operator to reduce data transmission.
* Auto-completion and syntax highlighting CLI.
* Pretrained Model Auto Serving.

### Examples

#### Tutorial 0: WordCount

Simplest NeuralSQL Example. In fact, the SQL executor will generates execution operator using MongoDB map-reduce. Prepare data uses `neuralsql -L wordcount` or `neuralsql --load-sample wordcount`.

```
SELECT content FROM text8.train TRAINER WordCount;
```

Word occurrences top 500:

```
SELECT content FROM text8.train TRAINER WordCount LIMIT 500;
```

#### Tutorial 1: Word2Vec

```
SELECT content FROM text8.train TRAINER Word2Vec;
```

We can use this example to build keyword recommendation engine. In next example, we will show you how to use MongoDB Stitch to serve word similarity request.

#### Tutorial 2: Twenty News Classifier

Prepare data uses `neuralsql -L classifier` or `neuralsql -L classifier[twenty_news]`.

```
SELECT content FROM twenty_news.train TRAINER classifier.MultinomialNB;
```

Or you can use a classifier attached by parameters:

```
SELECT content FROM twenty_news.train TRAINER classifier.SGDClassifier WITH loss='hinge', penalty='l2', random_state=42, max_iter=5, tol=None;
```

#### Tutorial 3: Chatbot

We can use MongoDB data to build a simple chatbot!


#### Configuration

If you want to use MongoDB Altas and MongoDB Stitch, you can set your username and password in `config.ini`.

#### Serverless

We can use serverless to query pretrained models. In `chatbot (MongoDB Stitch)` example, we will use MongoDB Stitch function to query pretrained model stored in MongoDB. You can connect MongoDB Stitch using `mongo` command.


```bash
mongo "mongodb://<username>:<password>@stitch.mongodb.com:27020/?authMechanism=PLAIN&authSource=%24external&ssl=true&appName=todo-tutorial1-uhdox:mongodb-atlas:local-userpass"
```

Then you can create a function in your Stitch app console.

```
exports = async function(text) {
  let res = await context.http.post({
    url: "http://www.der.ai/chatbot",
    form: {
      user_id: context.user.id,
      text: text
    }
  });
  
  return EJSON.parse(res.body.text());
};
```

You should deploy the simple chatbot service in your server. We deployed one in our server (maybe slow or down).

```bash
cd samples/chatbot_service
./run.sh
```

Finally, you can call this function in mongo shell.

```
db.runCommand({
    callFunction: "chatfunc",
    arguments: ["Hello World!"]
})
```

#### TODO

Lots of things to do. This is just a demo project. Do not used in production environment! However, welcome all of you to propose suggestions.

* TF-IDF Using MongoDB Map-Reduce

### Thanks

* CLI is inspired by [mycli](https://github.com/dbcli/mycli).
