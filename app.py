import json
import os

from flask import Flask, render_template


if os.path.isfile("db.json"):
    with open("db.json", "r", encoding="utf-8") as g:
        db = json.loads(g.readline())

app = Flask(__name__)


@app.route("/")
def main():
    return "Main"

@app.route("/goals/<goal>")
def goals(goal):
    return "Goal"

@app.route("/profiles/<id>")
def profiles(id):
    return render_template("profile.html", db_teacher= db[id])

@app.route("/request")
def request():
    return "Request"

@app.route("/request_done")
def request_done():
    return "Request_done"

@app.route("/booking/<id>")
def booking(id):
    return "Booking"

@app.route("/booking_done")
def booking_done():
    return "Booking_done"


if __name__ == '__main__':
    app.run()
