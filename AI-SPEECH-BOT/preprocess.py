# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:42:57 2020

@author: ItsTRD
"""
import tensorflow
import numpy
import nltk
from nltk.stem.lancaster import LancasterStemmer
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import tflearn


app = Flask("__main__")
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:root@localhost/flask_ai_bot"

db = SQLAlchemy(app)


class BotData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80))
    patterns = db.Column(db.Text)
    responses = db.Column(db.Text)
    context_set = db.Column(db.Text)
    status = db.Column(db.Integer)


data = {"intents": []}
result = BotData.query.all()
for i in result:
    if i.status == 1:
        d = {}
        d["tag"] = i.tag
        d["patterns"] = [i for i in i.patterns.split("|")]
        d["responses"] = [i for i in i.responses.split("|")]
        d["context_set"] = "" if i.context_set is None else i.context_set
        data["intents"].append(d)

stemmer = LancasterStemmer()

words = []
labels = []
docs_x = []
docs_y = []
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)
training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)


# tensorflow.reset_default_graph()
# net = tflearn.input_data(shape=[None, len(training[0])]) #40
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, 8)
# net = tflearn.fully_connected(net, len(output[0]), activation="softmax") #5
# net = tflearn.regression(net)

# model = tflearn.DNN(net)
# model.load('./log/model.tflearn')