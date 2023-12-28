from flask import render_template, request, redirect, session
from models import db, app, Question
from func import add_question, get_random_question, answers, comment

app.secret_key = 'random'


@app.before_request
def load():
    db.create_all()
    add_question()


@app.route('/')
def index():
    true_of_not = comment.bool
    comments = comment.komunikat
    pytanie = get_random_question()
    answer = answers(pytanie)[0]
    good_answer = answers(pytanie)[1]
    correct = Question.query.filter_by(user_correct=1).count()
    incorrect = Question.query.filter_by(user_correct=0).count()
    session['odpowiedz'] = good_answer
    session['pytanie'] = pytanie.question

    return render_template('page.html', komunikat=pytanie.question, answer=answer,
                           comments=comments, true_of_not=true_of_not, correct=correct, incorrect=incorrect)


@app.route('/answer', methods=['POST'])
def answerss():
    odpowiedz = session['odpowiedz']
    pytanie = session['pytanie']
    userrr = request.form.get('answer')
    question_obj = Question.query.filter_by(question=pytanie).first()
    if userrr == odpowiedz:
        comment.komunikat = 'Good!'
        comment.bool = True
        question_obj.user_correct = 1
        question_obj.asked = True
        db.session.commit()
    else:
        comment.komunikat = f"Not this time. Correct answer: {odpowiedz}"
        comment.bool = False
        question_obj.user_correct = 0
        question_obj.asked = True
        db.session.commit()
    return redirect('/')


@app.route('/favourite', methods=['POST'])
def favourite():
    pytanie = session['pytanie']
    click = request.form.get('fav')
    question_obj = Question.query.filter_by(question=pytanie).first()
    if click:
        comment.komunikat = f"Added '{pytanie}' to favourites."
        comment.bool = True
        question_obj.favourite = True
        db.session.commit()
    return redirect('/')

@app.route('/history.html')
def history():
    history_a = Question.query.all()
    counting = Question.query.count()
    return render_template("history.html", counting=counting, history_a=history_a)

@app.route('/history', methods=["POST"])
def history_view():
    click = request.form.get('type')
    if click == 'All':
        counting = Question.query.count()
        history_a =  Question.query.all()
    elif click == 'Correct':
        counting = Question.query.filter_by(user_correct=1).count()
        history_a = Question.query.filter_by(user_correct=1)
    elif click == 'Incorrect':
        counting = Question.query.filter_by(user_correct=0).count()
        history_a = Question.query.filter_by(user_correct=0)
    elif click == 'Favourite':
        counting = Question.query.filter_by(favourite=True).count()
        history_a = Question.query.filter_by(favourite=True)
    else:
        counting = Question.query.count()
        history_a = Question.query.all()
    return render_template("history.html",  counting=counting, history_a=history_a)

@app.route('/reset', methods=['POST'])
def reseting():
    reset = request.form.get('reset')
    if reset:
        Question.query.delete()
        db.session.commit()
        comment.komunikat = "DB deleted. "
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
