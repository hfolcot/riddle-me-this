import os, json, random
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "check out how random my string is" #Secret key is required for session

"""
Global Variables
"""
riddle_count = 1
all_users = {}

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
    
def reset_game(username):
    """
    Resets the game so the user can begin again
    """
    all_users[username]["current_riddle"] = 1
    all_users[username]["score"] = 0
    print(all_users)
    return all_users[username]["current_riddle"]

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
            session['username'] = request.form['username']
            with open("data/users.txt", "a") as f:
                current_user = request.form["username"]
                f.writelines(current_user + "\n")
                all_users[current_user] = {"name": current_user, "score": 0, "current_riddle": 1, "incorrect_answers": {}}
                print(all_users)
                return redirect(request.form["username"] + '/game')
    return render_template("index.html")

        
    
@app.route("/<username>/game", methods=["GET", "POST"])
#The page where the game will be played
def game(username):
    #Check to ensure user has entered their name, if not they are redirected back to index
    if 'username' in session:
        username = session['username']
        #Check to ensure there are still riddles left to show, ends the game if not
        if all_users[username]["current_riddle"] > 3:
            return redirect(username + "/endgame")
        all_riddles = get_all_riddles("data/riddles.json") #Creates a nested dict containing all riddles
        riddle = get_next_riddle(all_riddles, all_users[username]["current_riddle"]) #Selects the current riddle based on the count so far
        question = riddle["question"]
        answer = riddle["answer"]
        # Handle POST request
        if request.method == "POST":
            #check the answer is correct and if so redirect to the next question
            useranswer = request.form["answer"]
            if useranswer.lower() == answer:
                all_users[username]["current_riddle"] += 1
                all_users[username]["score"] += 1
                print(all_users[username])
                return redirect(username + "/game")
            #if incorrect the answer is printed below the answer box
            else:
                error = useranswer
                return render_template("game.html", question=question, error=error)
    else:
        return redirect("/")

    return render_template("game.html", question=question)
    
@app.route("/<username>/endgame", methods=["GET", "POST"])
#See the user score/high scores and get a chance to play again
def endgame(username):
    score = all_users[username]["score"]
    # Handle POST request
    if request.method == "POST":
        reset_game(username)
        return redirect(username + "/game")
    return render_template("endgame.html", score=score, username=username)


if __name__ == '__main__':       
    app.run(host=os.getenv("IP"), port=int(os.getenv("PORT")), debug=True)