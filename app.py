from flask import Flask, render_template, session, request, redirect, url_for
import os
import random

app = Flask(__name__)
app.secret_key = "supersecretkey_CHANGE_THIS"

CAPTCHA_FOLDER = "static/captcha"
DISPLAY_LIMIT = 10
MIN_CORRECT = 5
MAX_CORRECT = 6
SITE_PASSWORD = "frdkmXZJzas3258ZELDUHmkq"


@app.route("/")
def index():
    session.clear()

    all_images = [
        f for f in os.listdir(CAPTCHA_FOLDER)
        if f.lower().endswith(".png")
    ]

    correct_images = [img for img in all_images if img.startswith("ZELDA")]
    incorrect_images = [img for img in all_images if img.startswith("NOTZELDA")]

    random.shuffle(correct_images)
    random.shuffle(incorrect_images)

    max_possible_correct = min(len(correct_images), MAX_CORRECT)
    num_correct = random.randint(MIN_CORRECT, max_possible_correct)

    num_incorrect = DISPLAY_LIMIT - num_correct

    displayed_correct = correct_images[:num_correct]
    displayed_incorrect = incorrect_images[:num_incorrect]

    displayed_images = displayed_correct + displayed_incorrect
    random.shuffle(displayed_images)

    session["correct_displayed"] = displayed_correct

    return render_template("index.html", images=displayed_images)


@app.route("/verify", methods=["POST"])
def verify():
    selected = request.form.getlist("choice")
    correct_displayed = session.get("correct_displayed")

    if not correct_displayed:
        return redirect(url_for("index"))

    if set(selected) == set(correct_displayed):
        session["captcha_passed"] = True
        return redirect(url_for("password"))

    return redirect(url_for("index"))


@app.route("/password", methods=["GET", "POST"])
def password():
    if not session.get("captcha_passed"):
        return redirect(url_for("index"))

    if request.method == "POST":
        if request.form.get("password") == SITE_PASSWORD:
            session["authenticated"] = True
            return redirect(url_for("loading"))
        else:
            return render_template("password.html", error="Incorrect password.")

    return render_template("password.html")


@app.route("/loading")
def loading():
    if not session.get("authenticated"):
        return redirect(url_for("index"))

    return render_template("loading.html")


@app.route("/final")
def final():
    if not session.get("authenticated"):
        return redirect(url_for("index"))

    return render_template("final.html")


if __name__ == "__main__":
    app.run(port=8080, debug=True)