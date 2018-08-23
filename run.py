import os, json, random
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
#Welcome page containing username entry, instructions and current high scores
def index():
    error = ""
    # Handle POST request
    if request.method == "POST":
        usernames = open("data/users.txt").read()
        if request.form["username"] in usernames:
            error = "This username has already been taken"
            return render_template("index.html", error=error)
        else:
            with open("data/users.txt", "a") as f:
                f.writelines(request.form["username"] + "\n")
                return redirect('/game')
    return render_template("index.html")

@app.route("/game")
#The page where the game will be played
def game():
    get_all_riddles("data/riddles.json")


def get_all_riddles(riddle_file):
    """
    Load the riddles from the JSON file
    """
    with open(riddle_file, "r") as f:
        all_riddles = json.load(f)
        
app.run(host=os.getenv("IP"), port=int(os.getenv("PORT")), debug=True)