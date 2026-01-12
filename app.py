from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

def start_new_game(difficulty):
    if difficulty == "easy":
        max_val = 10
    elif difficulty == "medium":
        max_val = 50
    else:
        max_val = 100

    session["max"] = max_val
    session["number"] = random.randint(1, session["max"])
    session["attempts"] = 0
    session["points"] = 10
    session["difficulty"] = difficulty


@app.route("/", methods=["GET", "POST"])
def home():
    if "score" not in session:
        session["score"] = 0

    message = ""
    error = ""

    if "number" not in session:
        start_new_game("easy")

    if request.method == "POST":
        if "restart" in request.form:
            start_new_game(session.get("difficulty"))
            return redirect(url_for("home"))

        if "difficulty" in request.form:
            start_new_game(request.form["difficulty"])
            return redirect(url_for("home"))

        try:
            guess = int(request.form.get("guess", ""))
        except (ValueError, TypeError):
            error = "Please enter a valid number."
            return render_template(
                "index.html",
                message=message,
                error=error,
                score=session.get("score", 0),
                points=session.get("points", 0),
                max=session.get("max", 10),
                difficulty=session.get("difficulty"),
            )

        if guess < 1 or guess > session["max"]:
            error = f"Enter a number between 1 and {session['max']}."
        else:
            session["attempts"] = session.get("attempts", 0) + 1
            session["points"] = session.get("points", 10) - 1

            if guess < session["number"]:
                message = "Too low🔽😒"
            elif guess > session["number"]:
                message = "Too high🔼😁"
            else:
                message = "🎉 Correct!"
                session["score"] = session.get("score", 0) + session.get("points", 0)
                # start a new game with the same difficulty
                start_new_game(session.get("difficulty", "easy"))

    return render_template(
        "index.html",
        message=message,
        error=error,
        score=session.get("score", 0),
        points=session.get("points", 0),
        max=session.get("max", 10),
        difficulty=session.get("difficulty"),
    )


if __name__ == "__main__":
    app.run()
