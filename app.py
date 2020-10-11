import json
import os
import uuid
import random

from flask import Flask, render_template, request

from data import goals as gl, dow


def read_db():
    if os.path.isfile("db.json"):
        with open("db.json", "r", encoding="utf-8") as g:
            db = json.loads(g.readline())
            return db
    else:
        return None


def write_db(db=None):
    if db is not None:
        with open("db.json", "w", encoding="utf-8") as g:
            json.dump(db, g)


def write_db_request(db=None):
    if db is not None:
        with open("request.json", "w", encoding="utf-8") as g:
            json.dump(db, g)


def read_db_request():
    if os.path.isfile("request.json"):
        with open("request.json", "r", encoding="utf-8") as g:
            return json.load(g)
    else:
        with open("request.json", "w", encoding="utf-8") as g:
            stored_db = {"customers": {}}
            json.dump(stored_db, g)
        with open("request.json", "r", encoding="utf-8") as g:
            return json.load(g)


app = Flask(__name__)


@app.route("/")
def main():
    db = read_db()
    list_id = []
    for i in db:
        list_id.append(i)
    random.shuffle(list_id)
    return render_template("index.html", gl=gl, db=db, teacher_list=list_id[0:6])


@app.route("/goals/<goal>")
def goals(goal):
    db = read_db()
    db_goal = []
    for i in db:
        if goal in db[i]["goals"]:
            db_goal.append(db[i])
    print(db_goal)
    return render_template("goal.html", db=db_goal, goal=goal, gl=gl)


@app.route("/profiles/<pid>")
def profiles(pid):
    db = read_db()
    return render_template("profile.html", db_teacher=db[pid], gl=gl, dow=dow)


@app.route("/request")
def req():
    return render_template("request.html", gl=gl)


@app.route("/request_done", methods=["POST"])
def request_done():
    request_key = str(uuid.uuid4())
    rd = read_db_request()
    rd_new = {}
    for i in request.form.keys():
        rd_new[i] = request.form.get(i)
    rd["customers"][request_key] = rd_new
    write_db_request(db=rd)
    return render_template("request_done.html", customer=rd_new, gl=gl)


@app.route("/booking/<pid>/<day>/<time>")
def booking(pid, day, time):
    db = read_db()
    return render_template("booking.html",
                           db_teacher=db[pid],
                           day=dow[day],
                           time=time,
                           dow=day)


@app.route("/booking_done", methods=["POST"])
def booking_done():
    db = read_db()
    rd = {}
    for i in request.form.keys():
        rd[i] = request.form.get(i)
    db[rd["clientTeacher"]]["free"][rd["clientWeekday"]][rd["clientTime"]] = False
    write_db(db=db)
    return render_template("booking_done.html",
                           request_data=rd,
                           db_teacher=db[rd["clientTeacher"]],
                           day=dow)


if __name__ == '__main__':
    app.run()
