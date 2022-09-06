# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:42:57 2020

@author: ItsTRD
"""
from flask import Flask, render_template, request, flash, redirect, url_for
import numpy
import random
import speech_recognition as sr
import tensorflow
import tflearn
from flask_sqlalchemy import SQLAlchemy
import nltk
from nltk.stem.lancaster import LancasterStemmer
from flask_login import (
    LoginManager,
    AnonymousUserMixin,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from forms import LoginForm

# start App....
app = Flask(__name__)

# connect DB....
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:root@localhost/flask_ai_bot"
app.config["SECRET_KEY"] = "AiBotSecretKey"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# For voice recording
r = sr.Recognizer()
mic = sr.Microphone()

# connect login manager....
login_manager = LoginManager()
login_manager.login_view = "chatBotHtml"
login_manager.init_app(app)


data = {"intents": []}
model = None
X = None
Y = None
words = []
labels = []
docs_x = []
docs_y = []
training = []
output = []
stemmer = None

# english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
# trainer = ChatterBotCorpusTrainer(english_bot)
# trainer.train("chatterbot.corpus.english")

# Models for Tables....


class BotInputValues(db.Model):
    """ Table for recent parameters of graph """

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)


class BotData(db.Model):
    """ Table for ErrorData and responses """

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(80))
    patterns = db.Column(db.Text)
    responses = db.Column(db.Text)
    context_set = db.Column(db.Text)
    status = db.Column(db.Integer)

    def __init__(
        self, tag=None, patterns=None, responses=None, context_set=None, status=0
    ):
        self.tag = tag
        self.patterns = patterns
        self.responses = responses
        self.context_set = context_set
        self.status = status


class User(UserMixin, db.Model):
    """ Table for admin management """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))


@login_manager.user_loader
def load_user(user_id):
    """ This single function maintain entire the 'User session and management' """
    return User.query.get(int(user_id))


def preprocess():
    global data
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
    global stemmer
    stemmer = LancasterStemmer()
    global words
    words = []
    global labels
    labels = []
    global docs_x
    docs_x = []
    global docs_y
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
    global training
    training = []
    global output
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


def loadModel(x, y):
    global model
    tensorflow.reset_default_graph()
    net = tflearn.input_data(shape=[None, x])  # 40
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, y, activation="softmax")  # 5
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    model.load("log/model.tflearn")


preprocess()
result = BotInputValues.query.get(1)
X, Y = result.x, result.y
loadModel(X, Y)


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template(
        "index.html",
        is_login=current_user,
        total=BotData.query.all(),
        unsolved=BotData.query.filter_by(status=0).all(),
        solved=BotData.query.filter_by(status=1).all(),
    )


@app.route("/chatBotHtml")
def chatBotHtml():
    return render_template(
        "chatBot.html",
        is_login=current_user,
        unsolved=BotData.query.filter_by(status=0).all(),
    )


@app.route("/registerErrorHtml")
def registerErrorHtml():
    return render_template(
        "registerError.html",
        is_login=current_user,
        unsolved=BotData.query.filter_by(status=0).all(),
    )


@app.route("/addErrorHtml")
@login_required
def addErrorHtml():
    return render_template(
        "addError.html",
        is_login=current_user,
        unsolved=BotData.query.filter_by(status=0).all(),
    )


@app.route("/adminForm")
@login_required
def adminForm():
    result = BotData.query.all()
    return render_template(
        "adminTable.html",
        intents=result,
        is_login=current_user,
        unsolved=BotData.query.filter_by(status=0).all(),
    )


@app.route("/adminLogin")
def adminLogin():
    return render_template("login.html", login_form=LoginForm(request.form))


@app.route("/adminLogin", methods=["POST"])
def adminLoginPost():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(
            username=form.username.data, password=form.password.data
        ).first()
        if user:
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid login credentials")
    return redirect(url_for("adminLogin"))


@app.route("/adminLogout", methods=["POST"])
@login_required
def adminLogout():
    logout_user()
    return redirect(url_for("chatBotHtml"))


@app.errorhandler(404)
def error404(e):
    return render_template("404.html")


@app.errorhandler(401)
def error401(e):
    return render_template("401.html")


@app.errorhandler(500)
def error500(e):
    return render_template("500.html")


@app.route("/voice")
def get_voice_response():
    # userText = request.args.get('msg')
    with mic as source:
        print("Speak anything")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said", str(text))
        return str(text)

    except Exception as Error:
        print(Error)
        return Error

    return "Code error : Try Block Not Executed"


@app.route("/get")
def get_bot_response():
    userText = request.args.get("msg")
    global words
    global labels
    global data
    try:
        print("You typed", str(userText))

        results = model.predict([bag_of_words(userText, words)])[0]
        results_index = numpy.argmax(results)

        tag = labels[results_index]

        if results[results_index] > 0.7:

            for tg in data["intents"]:
                if tg["tag"] == tag:
                    responses = tg["responses"]

            global output1
            output1 = random.choice(responses)
        else:
            output1 = "I didn't get that plz try try reframing your query else raise a new error registration request from the pane above"

        print(str(output1))
        return str(output1)

    except Exception as Error:
        print(Error)
        return Error

    return userText
    # return str(english_bot.get_response(userText))


@app.route("/registerError")
@login_required
def register():
    if request.method == "GET":
        querry = request.args.get("querryInput")
        newEntry = BotData(patterns=querry)
        db.session.add(newEntry)
        failed = False
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            failed = True
        if failed:
            return "Database Failed Successfully!"
        return "Successfully added to Database!"


@app.route("/deleteRow")
@login_required
def delete():
    if request.method == "GET":
        idInput = int(request.args.get("idInput"))
        user = BotData.query.get(idInput)
        db.session.delete(user)
        failed = False
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            failed = True
        if failed:
            return "Object Not Deleted!"
        return "Object deleted successfully!"


@app.route("/editRow")
@login_required
def edit():
    if request.method == "GET":
        iid = int(request.args.get("id"))
        row = BotData.query.get(iid)
        row.tag = None if request.args.get("tag") == "None" else request.args.get("tag")
        row.patterns = (
            None
            if request.args.get("patterns") == "None"
            else request.args.get("patterns")
        )
        row.responses = (
            None
            if request.args.get("responses") == "None"
            else request.args.get("responses")
        )
        row.context_set = (
            None
            if request.args.get("context_set") == "None"
            else request.args.get("context_set")
        )
        row.status = int(request.args.get("status"))
        failed = False
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            failed = True
        if failed:
            return "Object editing failed!"
        return "Object Edited successfully!"


@app.route("/addRow")
@login_required
def add():
    if request.method == "GET":
        tag = None if request.args.get("tag") == "None" else request.args.get("tag")
        patterns = (
            None
            if request.args.get("patterns") == "None"
            else request.args.get("patterns")
        )
        responses = (
            None
            if request.args.get("responses") == "None"
            else request.args.get("responses")
        )
        context_set = (
            None
            if request.args.get("context_set") == "None"
            else request.args.get("context_set")
        )
        status = int(request.args.get("status"))
        newEntry = BotData(tag, patterns, responses, context_set, status)
        db.session.add(newEntry)
        failed = False
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            failed = True
        if failed:
            return "Object is not registered to database!"
        return "Object successfully added to database!"


@app.route("/trainBot")
@login_required
def train():
    global training
    global output
    global model
    global X
    global Y
    if request.method == "GET":
        preprocess()
        failed = False
        try:
            tensorflow.reset_default_graph()
            net = tflearn.input_data(shape=[None, len(training[0])])
            net = tflearn.fully_connected(net, 8)
            net = tflearn.fully_connected(net, 8)
            net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
            net = tflearn.regression(net)
            model_new = tflearn.DNN(net)
            model_new.fit(
                training, output, n_epoch=1000, batch_size=8, show_metric=True
            )
            try:
                result = BotInputValues.query.get(1)
                result.x = len(training[0])
                result.y = len(output[0])
                db.session.commit()
                model_new.save("log/model.tflearn")
            except Exception as l:
                print(l)
                failed = True
            if not failed:
                model = model_new  # here
                X, Y = len(training[0]), len(output[0])
            else:
                db.session.rollback()
                db.session.flush()
        except Exception as e:
            print(e)
            failed = True
        if failed:
            return "Chat bot training failed!"
        return "Chat bot trained successfully!"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
