from flask import Flask, render_template, request, make_response
import sqlite3
from rake_nltk import Rake
import nltk
from nltk.corpus import wordnet
import PyDictionary
import json
from nltk.stem import WordNetLemmatizer
import os

app = Flask(__name__)


# SQLite Database
def create_questions_table():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS QuestionsTable (id INTEGER PRIMARY KEY,Question TEXT,Answer TEXT, '
                 'Key TEXT)')
    conn.close()


# CALL TO TABLE CREATE
create_questions_table()


def load_question(number):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f"select Question from QuestionsTable where id={number}")
    return cur.fetchone()


def load_answer(number):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f"select Answer from QuestionsTable where id={number}")
    return cur.fetchone()


def load_key(number):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f"select Key from QuestionsTable where id={number}")
    return cur.fetchone()


questions = [
    "what is AI?"
]
answers = [
    'The theory and development of computer systems able to perform tasks normally requiring human intelligence,'
    'such as visual perception, speech recognition, decision-making, and translation between languages.'
]
KEY = [{'human': 5, 'recognition': 5, 'computer': 5, 'able': 5, 'visual': 5, 'speech': 5, 'task': 5, 'translation': 5,
        'making': 5,
        'perception': 5, 'language': 5, 'development': 5, 'perform': 5, 'normally': 5, 'intelligence': 5, 'decision': 5,
        'system': 5,
        'theory': 8, 'requiring': 7}]


# GET ITEM COUNT
def items_present():
    conn = sqlite3.connect('database.db')
    x = conn.execute('select count(Question) from QuestionsTable')
    count = x.fetchone()[0]
    conn.close()
    return count


def break_phrases(list):
    a = []
    for x in list:
        if len(x.split()) == 1:
            a.append(x)
        else:
            a.extend(x.split())
    return a


def lematize(lista):
    w = WordNetLemmatizer()
    a = list(map(w.lemmatize, lista))
    return a


@app.route("/", methods=['GET'])
def index():
    count_itm = items_present()
    if request.method == 'GET' and request.args.get("q") != "" and request.args.get("q") is not None:
        index_question = request.args.get("q")
        if int(index_question) <= count_itm:
            template = render_template("index.html", questionsCount=count_itm, questionToLoad=request.args.get("q"),
                                   questionData=load_question(index_question))
            response = make_response(template);
            response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
            return response;

    template = render_template("index.html", questionsCount=count_itm)
    response = make_response(template);
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
    return response;


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/checkAnswer")
def check():
    max_score = 10
    if request.method == 'GET' and request.args.get("a") != "" and request.args.get("a") is not None:
        answer_data = request.args.get("a")
        question_index = int(request.args.get("q"))
        trained_data, test_data = Rake(), Rake()
        load_ans = load_answer(question_index)[0]
        trained_data.extract_keywords_from_text(load_ans)
        test_data.extract_keywords_from_text(answer_data)

        testlist = []
        trainlist = []

        test_data_keywords = lematize(break_phrases(test_data.get_ranked_phrases()))
        for x in test_data_keywords:
            testlist.append(x)
        result = 0
        dict = eval(load_key(question_index)[0])
        z = 0
        for x in testlist:

            if x in dict.keys():
                print(x)
                result = result + (dict[x] * max_score) / 100
                print(result, dict[x])
            else:
                syn = PyDictionary.PyDictionary().synonym(testlist[z])
                if syn == None:
                    continue
                print(syn)
                for j in syn:
                    if j in testlist:
                        print(trainlist[question_index - 1], j)
                        print(dict)
                        dict[j] = (dict[x] * max_score) / 100
                        result = result + dict[j] * max_score
                        matched.append(question_index - 1)
            z += 1
        return str(result) + "#" + load_ans


@app.route("/loadDemo")
def add_demo_questions():
    msg = "UNKNOWN"
    conn = sqlite3.connect('database.db')
    try:
        for i in range(0, len(questions)):
            conn.execute("INSERT INTO QuestionsTable (Question,Answer,Key) VALUES(?, ?, ?)",
                         (questions[i], answers[i], json.dumps(KEY[i])))
            conn.commit()
            msg = "ADDED"
    except:
        return "ERROR"
    finally:
        conn.close()
        return msg


@app.route("/emptyTable")
def delete_table_data():
    con = sqlite3.connect("database.db")
    con.execute('delete from QuestionsTable')
    con.commit()
    con.close()
    return "DONE"


def add_data(data_listing, each_val):
    values_list = []
    z = 0
    for x in range(0, len(data_listing)):
        values_list.append(each_val)
        z += each_val
    values_list[0] += 100 - sum(values_list)
    return values_list


def add_to_table(question, answer, key):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO QuestionsTable (Question,Answer,Key) VALUES(?, ?, ?)",
                 (question, answer, key))
    conn.commit()
    conn.close()


@app.route("/addQuestion", methods=['GET'])
def add_question():
    answer_data = request.args.get("a")
    question_data = request.args.get("q")
    r = Rake()
    r.extract_keywords_from_text(answer_data)
    data_list = lematize(break_phrases(r.get_ranked_phrases()))
    each_value = int(100 / len(data_list))
    values_list = add_data(data_list, each_value)
    dict_data = {data_list[i]: values_list[i] for i in range(0, len(values_list))}
    add_to_table(question_data, answer_data, json.dumps(dict_data))
    return dict_data


if __name__ == '__main__':
    app.run(debug=True,port=int(os.environ.get('PORT', 8080)))
