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
    """
    Selects an entry from the nested dictionary and returns it as a riddle with a question and answer
    """
    count = str(riddle_count)
    riddle = riddles[count]
    return riddle
    
def reset_game():
    """
    Resets the game so the user can begin again
    """
    global riddle_count
    riddle_count = 1
    return riddle_count

@app.route("/", methods=["GET", "POST"])
#Welcome page containing username entry, instructions and current high scores
def index():
    error = ""
    # Handle POST request: ensures that username is unique and if so it is entered into the users.txt file
    # If not unique an error is shown on the page and the user must try again
    if request.method == "POST":
        usernames = open("data/users.txt").read()
        if request.form["username"] in usernames:
            error = "This username has already been taken"
            return render_template("index.html", error=error)
        else:
            with open("data/users.txt", "a") as f:
                f.writelines(request.form["username"] + "\n")
                return redirect(request.form["username"] + '/game')
    return render_template("index.html")

        
    
@app.route("/<username>/game", methods=["GET", "POST"])
#The page where the game will be played
def game(username):
    global riddle_count
    if riddle_count > 3:
        return redirect(username + "/endgame")
    all_riddles = get_all_riddles("data/riddles.json") #Creates a nested dict containing all riddles
    riddle = get_next_riddle(all_riddles, riddle_count) #Selects the current riddle based on the count so far
    question = riddle["question"]
    answer = riddle["answer"]
    # Handle POST request
    if request.method == "POST":
        useranswer = request.form["answer"]
        if useranswer.lower() == answer:
            riddle_count += 1
            return redirect(username + "/game")
        else:
            error = useranswer
            return render_template("game.html", question=question, error=error)


    return render_template("game.html", question=question)
    
@app.route("/<username>/endgame", methods=["GET", "POST"])
#See the high scores and get a chance to play again
def endgame(username):
    # Handle POST request
    if request.method == "POST":
        reset_game()
        return redirect(username + "/game")
    return render_template("endgame.html")


if __name__ == '__main__':       
    app.run(host=os.getenv("IP"), port=int(os.getenv("PORT")), debug=True)