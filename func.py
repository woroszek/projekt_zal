import requests
from models import Question, db
import random
import html


def add_question():
    if Question.query.filter_by(asked=False).count() == 0:
        try:
            response = requests.get('https://opentdb.com/api.php?amount=10&category=9&type=multiple')
            tab = response.json()

            for i in range(10):
                result = tab['results'][i]
                question = Question(
                    question=html.unescape(result["question"]),
                    correct_answer=html.unescape(result["correct_answer"]),
                    incorrect_answers=html.unescape(result["incorrect_answers"])
                )
                db.session.add(question)
                db.session.commit()
        except KeyError:
            pass


def get_random_question():
    questions = Question.query.filter_by(asked=False).all()
    question = random.choice(questions)
    db.session.commit()
    return question


def answers(question):
    incorrect = [x for x in question.incorrect_answers]
    correct = question.correct_answer
    answers = [correct] + incorrect
    ran_answers = html.unescape(random.sample(answers, 4))
    return ran_answers, correct


class Comment:
    def __init__(self):
        self.komunikat = "Tutaj zobaczysz komunikaty."
        self.bool = False


comment = Comment()
