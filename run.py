import os, json, random
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

"""
Global Variables
"""
riddle_count = 1

"""
Main Game functions
"""

def get_all_riddles(riddle_file):
    """
    Load the riddles from the JSON file
    """
    with open(riddle_file, "r") as f:
        all_riddles = json.load(f)
    return all_riddles
    
def get_next_riddle(riddles, riddle_count):
    count = str(riddle_count)
    riddle = riddles[count]
    return riddle

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

        
    
@app.route("/game", methods=["GET", "POST"])
#The page where the game will be played
def game():
    global riddle_count
    if riddle_count > 20:
        return redirect("/endgame")
    all_riddles = get_all_riddles("data/riddles.json")
    riddle = get_next_riddle(all_riddles, riddle_count)
    question = riddle["question"]
    answer = riddle["answer"]
     # Handle POST request
    if request.method == "POST":
        if request.form["answer"] == answer:
            riddle_count += 1
            return redirect("/game")
        else:
            error = "Incorrect"
            return render_template("game.html", question=question, error=error)


    return render_template("game.html", question=question)
    
@app.route("/endgame")
#See the high scores and get a chance to play again



if __name__ == '__main__':       
    app.run(host=os.getenv("IP"), port=int(os.getenv("PORT")), debug=True)