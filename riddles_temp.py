import json

def get_all_riddles(riddle_file):
    """
    Load the riddles from the JSON file
    """
    with open(riddle_file, "r") as f:
        all_riddles = json.load(f)
    for item in all_riddles:
        print(all_riddles[item])


get_all_riddles("data/riddles.json")