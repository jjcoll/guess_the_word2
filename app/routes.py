from app import app, db
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from app.models import User
from app.forms import RegisterForm, LoginForm
from flask_login import login_user
from app.game_logic import start_new_game, print_board, check_board


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/play")
def play_page():

    letters = "abcdefghijklmnopqrstuvwxyz"
    letters_list = list(letters)

    start_new_game("animals.txt")

    print(session["survival"])

    return render_template(
        "play.html",
        letters_list=letters_list,
        board=print_board(session["board"]),
        lives=session["lives"],
        wordlist=session["wordsfile"],
        survival=session["survival"],
        score=session["score"],
    )


@app.route("/guess", methods=["POST"])
def guess_letter():
    # Access JSON data

    board = session["board"]
    word = session["word"]
    previous_lives = session["lives"]
    slected_letter = request.json.get("letter")

    session["started"] = True

    board, lives, won = check_board(slected_letter, board, word, previous_lives)

    if lives != previous_lives:
        update_lives = True
    else:
        update_lives = False

    data_return = {
        "updatedWord": print_board(board),
        "updateLives": update_lives,
        "lives": lives,
        "won": won,
    }

    return jsonify(data_return)


@app.route("/game-over")
def game_over():

    outcome = request.args.get("outcome")
    print(session["won"])

    if outcome == "win" and session["won"]:
        return render_template(
            "gameover-win.html",
            lives=session["lives"],
            score=session["score"],
            survival=session["survival"],
        )
    elif outcome == "win" and not session["won"]:
        flash("This will not work, please play honestly!", "danger")
        return redirect(url_for("play_page"))
    else:
        # reset score and survival because you lost
        session["score"] = 0
        session["survival"] = False
        return render_template(
            "gameover-lose.html",
            word=session["word"],
            score=session["score"],
            survival=session["score"],
        )


@app.route("/submit")
def submit_page():
    return render_template("register.html")


@app.route("/trigger-survival", methods=["POST"])
def trigger_survival():
    survival = request.json.get("survival")

    if not session["started"]:
        session["survival"] = survival

    # return redirect(url_for("play_page"))
    return jsonify(
        {
            "survival": session["survival"],
            "started": session["started"],
            "score": session["score"],
        }
    )


@app.route("/register", methods=["POST", "GET"])
def register_page():

    form = RegisterForm()

    if form.validate_on_submit():
        user_to_add = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password1.data,
        )

        db.session.add(user_to_add)
        db.session.commit()

    return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        # validate login details
        # check user exists
        user_to_check = User.query.filter_by(username=form.username.data).first()
        if user_to_check:
            # user exists check password match
            if user_to_check.check_password(form.password.data):
                # user and password match => login user
                print("Login successful")
                flash(f"User {user_to_check.username} logged in successfuly", "success")

                # login user
                login_user(user_to_check)

                next = request.args.get("next")

                return redirect(next or url_for("home_page"))

            else:
                # password is not correct
                flash("Password is not correct", "danger")
        else:
            # user does not exist
            flash("User does not exist", "danger")

    return render_template("login.html", form=form)
