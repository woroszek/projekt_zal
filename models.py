from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
    incorrect_answers = db.Column(db.JSON)
    asked = db.Column(db.Boolean, default=False)
    favourite = db.Column(db.Boolean, default=False)
    user_correct = db.Column(db.Integer, default=2)