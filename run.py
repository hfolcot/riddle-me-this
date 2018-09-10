import os, json, random, datetime
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "check out how random my string is" #Secret key is required for session

"""
Global Variables
"""
riddle_count = 1
all_users = {}
all_current_scores = {"Player 1": {"date": "2018-09-10", "score": 0}} #Sample entry

"""
Main Game functions
"""
def get_data(file):
    """
    Load the required data (riddles/scores) from a json file
    """
    with open(file, "r") as f:
        data = json.load(f)
    return data
    
def order_high_scores(data):
    """
    Order the scores by largest to smallest and make the top ten available for the high scores table
    """
    
    ordered_scores = sorted(data, key=lambda x: (data[x]["score"], data[x]["date"]), reverse=True)
    return ordered_scores[:10]
    
def add_to_scores(file, user, score):
    """
    Add the current user's score to the scores.json file
    """
    now = str(datetime.date.today())
    all_current_scores[user]= {"score" : score, "date" : now} #Adds a new entry to the all_current_scores dict
    with open("data/scores.json", "w") as f:
        json.dump(all_current_scores, f)
    
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
    all_scores = get_data("data/scores.json")
    ordered_scores = order_high_scores(all_scores)
    return render_template("index.html", all_scores=all_scores, ordered_scores=ordered_scores)

        
    
@app.route("/<username>/game", methods=["GET", "POST"])
#The page where the game will be played
def game(username):
    #Check to ensure user has entered their name, if not they are redirected back to index
    if 'username' in session:
        username = session['username']
        #Check to ensure there are still riddles left to show, ends the game if not
        if all_users[username]["current_riddle"] > 3:
            add_to_scores("data/scores.json", username, all_users[username]["score"])
            return redirect(username + "/endgame")
        all_riddles = get_data("data/riddles.json") #Creates a nested dict containing all riddles
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
    all_scores = get_data("data/scores.json")
    ordered_scores = order_high_scores(all_scores)
    return render_template("endgame.html", score=score, username=username, all_scores=all_scores, ordered_scores=ordered_scores)


if __name__ == '__main__':       
    app.run(host=os.getenv("IP"), port=int(os.getenv("PORT")), debug=True)