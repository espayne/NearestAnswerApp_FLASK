from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql import text
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = "neartobull3216"

db_name = 'nttb_answers.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    table_name = 'nttb_answers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    answer = db.Column(db.Float)
    absdiff = db.Column(db.Float)

    def __init__(self, name, answer, absdiff):
        self.name = name
        self.answer = answer
        self.absdiff = absdiff

db.create_all()

@app.route("/hello")
def index():
    flash("Hello, who are you?")
    return render_template("front.html")

@app.route("/question", methods=['POST', 'GET'])
def greeter():
    flash(str(request.form['name_input']) + ", how many functioning London Underground stations are there?")
    session['nttb_name'] = request.form['name_input']
    return (render_template("question.html"))

@app.route("/thank-you", methods=['POST', 'GET'])
def thanks():
    nttb_name = session.get('nttb_name', None)
    nttb_answers = User(nttb_name, request.form['answer_input'], abs(float(request.form['answer_input']) - 272))
    db.session.add(nttb_answers)
    db.session.commit()
    session.clear()
    return render_template("end.html")

@app.route("/results", methods=['POST', 'GET'])
def thanks2():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['admin'] = request.form['username']
            return redirect(url_for('inventory'))
        else:
            error = 'Nope! Wrong login'
    return render_template("results.html", error = error)

@app.route('/results-table')
def inventory():
    if 'admin' not in session:
        return redirect(url_for('index'))
    else:
        session.clear()
        guesses = User.query.order_by(desc(User.absdiff)).all()
        worstguess = User.query.order_by(desc(User.absdiff)).limit(1)
        return render_template('resultstable.html', guesses=guesses, worstguess=worstguess)
