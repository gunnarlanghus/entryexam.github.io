import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///room.db")

@app.route("/")
def room():
    return render_template("room.html")

@app.route("/biology")
def biology():
    return render_template("biology.html")

@app.route("/blanks", methods=["GET", "POST"])
def blanks():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("deciphered"):
            return apology("must provide deciphered message", 403)

        data = db.execute("SELECT tries FROM tries WHERE puzzle = 'blanks'")
        tries = int(data[0]["tries"]) + 1

        db.execute("UPDATE tries SET tries = ? WHERE puzzle = 'blanks'",
                          tries)

        key = "jdrpkinj rpdtcgkpdan"

        if request.form.get("deciphered") != key:
            if tries < 3:
                return apology("code incorrect (try solving the concentration problem for K)", 403)
            elif (3 < tries < 5):
                return apology("code incorrect (try setting the cipher wheel so K is equal to what K equals in the concentration problem)", 403)
            elif tries > 7:
                return apology("code incorrect (try solving quantum numbers to find the concentrations of S, P, D, & F, then solve the concentration problem for K)", 403)
        else:
            db.execute("INSERT INTO clues (clue, value) VALUES('message', ?)",
                          key)

        return redirect("/wheelback")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("blanks.html")

@app.route("/bookshelf")
def bookshelf():
    return render_template("bookshelf.html")

@app.route("/chemistry")
def chemistry():
    return render_template("chemistry.html")

@app.route("/clues")
def clues():
   data = db.execute("SELECT * FROM clues")
   return render_template("clues.html", len=len(data), data=data)

@app.route("/computer")
def computer():
    return render_template("computer.html")

@app.route("/concentration", methods=["GET", "POST"])
def concentration():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("K"):
            return apology("must provide K value", 403)

        data = db.execute("SELECT tries FROM tries WHERE puzzle = 'concentration'")
        tries = int(data[0]["tries"]) + 1

        db.execute("UPDATE tries SET tries = ? WHERE puzzle = 'concentration'",
                          tries)

        if request.form.get("K") != 20:
            if tries <= 3:
                return apology("K incorrect (try solving the table)", 403)
            elif tries > 3:
                return apology("K incorrect (try solving the table and using the subshell energy levels as concentrations for S, P, D, and F)", 403)
        else:
            db.execute("INSERT INTO clues (clue, value) VALUES('K Value', '20')")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("concentration.html")

@app.route("/cryptography", methods=["GET", "POST"])
def cryptography():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        db.execute("INSERT INTO clues (clue, value) VALUES('Book', 'Keywords by Raymond Williams')")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("cryptography.html")

@app.route("/desk")
def desk():
    return render_template("desk.html")

@app.route("/engineering")
def engineering():
    return render_template("engineering.html")

@app.route("/lock1", methods=["GET", "POST"])
def lcok1():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("IMF"):
            return apology("must provide IMF", 403)

        data = db.execute("SELECT tries FROM tries WHERE puzzle = 'lock1'")
        tries = int(data[0]["tries"]) + 1

        db.execute("UPDATE tries SET tries = ? WHERE puzzle = 'lock1'",
                          tries)

        if request.form.get("IMF") != "Dipole-Dipole":
            if tries == 1:
                return apology("IMF incorrect (try deciphering the message from blanks using the hint on the back of the cipher wheel)", 403)
            elif tries == 2:
                db.execute("UPDATE tries SET tries = 0")
                db.execute("DELETE FROM clues")
                return render_template("fail.html")
        else:
            db.execute("INSERT INTO clues (clue, value) VALUES('IMF', 'Dipole-Dipole')")

        return redirect("/lock2")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("lock1.html")


@app.route("/lock2", methods=["GET", "POST"])
def lock2():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("formula"):
            return apology("must provide formula", 403)

        data = db.execute("SELECT tries FROM tries WHERE puzzle = 'lock2'")
        tries = int(data[0]["tries"]) + 1

        db.execute("UPDATE tries SET tries = ? WHERE puzzle = 'lock2'",
                          tries)

        if request.form.get("formula") != "NCl3":
            if tries <= 2:
                return apology("Formula incorrect (Have you deciphered the message from the numbers?)", 403)
            elif (2 < tries < 5):
                return apology("code incorrect (Check the bookshelf for a hint on what kind of cipher the message from the numbers uses)", 403)
            elif (5 <= tries < 8):
                return apology("code incorrect (Check the back of the cipher wheel for the keyword of the cipher)", 403)
            elif tries >= 8:
                return apology("code incorrect (The message from the numbers uses a keyword cipher, where the keyword is the name of the compound on the back of the cipher wheel. Use the poster to help name that compound.)", 403)
        else:
            db.execute("UPDATE tries SET tries = 0")
            db.execute("DELETE FROM clues")
            return render_template("pass.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("lock2.html")

@app.route("/physics")
def physics():
    return render_template("physics.html")

@app.route("/poster")
def poster():
    return render_template("poster.html")

@app.route("/table", methods=["GET", "POST"])
def table():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("X1"):
            return apology("must provide all values", 403)
        elif not request.form.get("X2"):
            return apology
        elif not request.form.get("X3"):
            return apology("must provide all values", 403)
        elif not request.form.get("X4"):
            return apology("must provide all values", 403)

        data = db.execute("SELECT tries FROM tries WHERE puzzle = 'table'")
        tries = int(data[0]["tries"]) + 1

        db.execute("UPDATE tries SET tries = ? WHERE puzzle = 'table'",
                          tries)
        answer = [request.form.get("X1"), request.form.get("X2"), request.form.get("X3"), request.form.get("X4")]
        key = ["1s", "4f", "2p", "5d"]

        if answer != key:
            if tries <= 3:
                return apology("numbers incorrect", 403)
            elif tries > 3:
                return apology("numbers incorrect (make sure your answers are formatted like '5s')", 403)
        else:
            db.execute("INSERT INTO clues (clue, value) VALUES('numbers', ?)",
                          "X1 = 1s, X2 = 4f, X3 = 2p, X4 = 5d")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("table.html")

@app.route("/wheel")
def wheel():
    return render_template("wheel.html")

@app.route("/wheelback", methods=["GET", "POST"])
def wheelback():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        db.execute("INSERT INTO clues (clue, value) VALUES('Keyword', 'https://www.chemspider.com/ImagesHandler.ashx?id=259&w=250&h=250')")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("wheelback.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
