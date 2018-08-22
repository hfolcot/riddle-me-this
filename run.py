import os, json, random
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

app.run(host=os.getenv("IP"), port=int(os.getenv("PORT")), debug=True)


def get_all_riddles(riddle_file):
    """
    Load the riddles from the JSON file
    """
    with open(riddle_file, "r") as f:
        all_riddles = json.load(f)

def main():
    get_all_riddles("data/riddles.json")
    
if __name__ == "__main__":
    main()
    """
    Ensure the program only runs if specified by run.py
    """

    