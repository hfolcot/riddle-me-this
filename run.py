import os, json, datetime
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "check out how random my string is" #Secret key is required for session


"""
Global Variables
"""
riddle_count = 1
all_users = {}
all_current_scores = {}




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
    all_current_scores = get_data("data/scores.json")
    now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    today = str(datetime.date.today())
    entry = user + now #allows for a unique entry in high scores dict
    all_current_scores[entry]= {"name": user, "score" : score, "date" : today} #Adds a new entry to the all_current_scores dict
    with open("data/scores.json", "w") as f:
        json.dump(all_current_scores, f)
        
def create_new_user(username):
    with open("data/users.txt", "a") as f:
        current_user = username
        f.writelines(current_user + "\n")
        all_users[current_user] = {"name": current_user, "score": 0, "current_riddle": 1, "incorrect_answers": [], "correct": "yes"}
        return all_users
    
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


    
"""
Pages
"""

@app.route("/", methods=["GET", "POST"])
#Welcome page containing username entry, instructions and current high scores
def index():
    all_scores = get_data("data/scores.json")
    ordered_scores = order_high_scores(all_scores)
    error = ""
    # Handle POST request: ensures that username is unique and if so it is entered into the users.txt file
    # If not unique an error is shown on the page and the user must try again
    if request.method == "POST":
        usernames = open("data/users.txt").readlines()
        for item in usernames:
            name = item.rstrip('\n')
            if request.form["username"] == name:
                error = "That username has already been taken."
                return render_template("index.html", error=error, all_scores=all_scores, ordered_scores=ordered_scores)
        else:
            username = request.form["username"]
            
            #Input sanitised to prevent bad characters from interfering with the URLs
            badchars = ["\\", "/", "=", "%", "?"]
            for i in badchars:
                if i in username:
                    username = username.replace(i, "-")
                    
            session['username'] = username
            create_new_user(username)
            return redirect(username + '/game')
    return render_template("index.html", all_scores=all_scores, ordered_scores=ordered_scores)

        
    
@app.route("/<username>/game", methods=["GET", "POST"])
#The page where the game will be played
def game(username):
    #Checks to ensure user has entered their name, if not they are redirected back to index
    #This prevents users from trying to access the game by typing straight into the address bar
    if 'username' in session:
        username = session['username']
        
        #Check to ensure there are still riddles left to show, ends the game if not
        if all_users[username]["current_riddle"] > 20:
            add_to_scores("data/scores.json", username, all_users[username]["score"])
            return redirect(username + "/endgame")
            
        all_riddles = get_data("data/riddles.json") #Creates a nested dict containing all riddles
        riddle = get_next_riddle(all_riddles, all_users[username]["current_riddle"]) #Selects the current riddle based on the count so far
        question = riddle["question"]
        question = question.replace('\n','<br>')
        answer = riddle["answer"]
        
        # Handle POST request
        if request.method == "POST":
            #check the answer is correct and if so redirect to the next question
            if request.form["action"] == "go":
                useranswer = request.form["answer"]
                if useranswer.lower().rstrip() == answer:
                    all_users[username]["current_riddle"] += 1
                    all_users[username]["score"] += 1
                    all_users[username]["incorrect_answers"] = []
                    all_users[username]["correct"] = "yes"
                    return redirect(username + "/game")
                    
                #if incorrect the answer is printed below the answer box
                else:
                    all_users[username]["incorrect_answers"].append(useranswer)
                    all_users[username]["correct"]="no"
                    return render_template("game.html", question=question, error=all_users[username]["incorrect_answers"], username=username, qnumber=all_users[username]["current_riddle"], correct=all_users[username]["correct"], score=all_users[username]["score"])
                    
            #if player opts to skip the question the next riddle will be shown but no points will be given
            elif request.form["action"] == "skip":
                all_users[username]["current_riddle"] += 1
                all_users[username]["incorrect_answers"] = []
                all_users[username]["correct"]="skip"
                return redirect(username + "/game")
            elif request.form["action"] == "logout":
                #Logs out the current user and returns to index
                reset_game(username)
                session.pop(username, None)
                return redirect("/")
    else:
        return redirect("/") #redirects user to index to enter their name

    return render_template("game.html", question=question, username=username, qnumber=all_users[username]["current_riddle"], correct=all_users[username]["correct"], score=all_users[username]["score"])
    
@app.route("/<username>/endgame", methods=["GET", "POST"])
#See the user score/high scores and get a chance to play again
def endgame(username):
    score = all_users[username]["score"]
    
    # Handle POST request
    if request.method == "POST":
        if request.form["action"] == "replay":
            reset_game(username)
            return redirect(username + "/game")
        elif request.form["action"] == "end":
            #Logs out the current user and returns to index
            reset_game(username)
            session.pop(username, None)
            return redirect("/")
            
    all_scores = get_data("data/scores.json")
    ordered_scores = order_high_scores(all_scores)
    return render_template("endgame.html", score=score, username=username, all_scores=all_scores, ordered_scores=ordered_scores)



#Use the IF statement below to prevent the file from executing fully when imported by other modules
if __name__ == '__main__':       
    app.run(host=os.getenv("IP"), port=int(os.getenv("PORT")), debug=False)