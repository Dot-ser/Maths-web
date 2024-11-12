from flask import Flask, render_template, request, redirect, url_for, session
import random
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

LEVELS = {
    "easy": {"timeout": 10, "min": 1, "max": 10},
    "medium": {"timeout": 7, "min": 1, "max": 20},
    "hard": {"timeout": 5, "min": 10, "max": 50},
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/quiz', methods=['POST'])
def quiz():
    level = request.form.get("level")
    if level not in LEVELS:
        return redirect(url_for("index"))

    session["level"] = level
    session["score"] = 0
    session["total_questions"] = 10  # Set total questions here
    session["current_question"] = 0  # Track current question count
    session["start_time"] = time.time()

    return redirect(url_for("question"))

@app.route('/question')
def question():
    level = session.get("level")
    if not level:
        return redirect(url_for("index"))

    settings = LEVELS[level]
    num1 = random.randint(settings["min"], settings["max"])
    num2 = random.randint(settings["min"], settings["max"])
    session["answer"] = num1 + num2
    session["current_question"] += 1

    # If current question exceeds total questions, end quiz
    if session["current_question"] > session["total_questions"]:
        return redirect(url_for("result"))

    return render_template("quiz.html", num1=num1, num2=num2, timeout=settings["timeout"])

@app.route('/submit', methods=['POST'])
def submit():
    user_answer = request.form.get("answer")
    try:
        user_answer = int(user_answer)
    except ValueError:
        user_answer = None

    if user_answer == session.get("answer"):
        session["score"] += 1

    if time.time() - session["start_time"] > 30:
        return redirect(url_for("result"))

    return redirect(url_for("question"))

@app.route('/result')
def result():
    score = session.get("score", 0)
    total_questions = session.get("total_questions", 10)
    return render_template("result.html", score=score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
