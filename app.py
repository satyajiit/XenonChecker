from flask import Flask, render_template, request, make_response
import sqlite3
from rake_nltk import Rake
import nltk
from nltk.corpus import wordnet
import PyDictionary
import json
from nltk.stem import WordNetLemmatizer
import os
from datetime import datetime
from functools import wraps, update_wrapper

app = Flask(__name__)


# SQLite Database
def create_questions_table():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS QuestionsTable (id INTEGER PRIMARY KEY,Question TEXT,Answer TEXT, '
                 'Key TEXT)')
    conn.close()


# CALL TO TABLE CREATE
create_questions_table()


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)


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
    "What is Internet?"
]
answers = [
    'A global computer network providing a variety of information and communication facilities, consisting of interconnected networks using standardized communication protocols.'
]
KEY = [{
  "communication": 7, 
  "computer": 16, 
  "consisting": 7, 
  "facility": 7, 
  "global": 7, 
  "information": 7, 
  "interconnected": 7, 
  "network": 7, 
  "protocol": 7, 
  "providing": 7, 
  "standardized": 7, 
  "using": 7, 
  "variety": 7
}]


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
@nocache
def index():
    count_itm = items_present()
    if request.method == 'GET' and request.args.get("q") != "" and request.args.get("q") is not None:
        index_question = request.args.get("q")
        if int(index_question) <= count_itm:
            return render_template("index.html", questionsCount=count_itm, questionToLoad=request.args.get("q"),
                                   questionData=load_question(index_question))

    return render_template("index.html", questionsCount=count_itm)
 


@app.route("/about")
@nocache
def about():
    return render_template("about.html")


@app.route("/add")
@nocache
def add():
    return render_template("add.html")


@app.route("/checkAnswer")
@nocache
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
        if result > 10:
            result = 10;
        return str(result) + "#" + load_ans


@app.route("/loadDemo")
@nocache
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
@nocache
def delete_table_data():
    con = sqlite3.connect("database.db")
    con.execute('delete from QuestionsTable')
    con.commit()
    con.close()
    return "DONE"


def add_data(data_listing, each_val):
    values_list2 = []
    z = 0
    for x in range(0, len(data_listing)):
        values_list2.append(each_val)
        z += each_val
    values_list2[0] += (100 - sum(values_list2))
    print(values_list2)
    return values_list2


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
    data_list = list(set(data_list))
    each_value = int(100 / len(data_list))
    values_list = add_data(data_list, each_value)
    print(values_list)
    print(data_list)
    dict_data = {data_list[i]: values_list[i] for i in range(0, len(data_list))}
    print(dict_data)
    add_to_table(question_data, answer_data, json.dumps(dict_data))
    return dict_data

#host='0.0.0.0'

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 8080)))
