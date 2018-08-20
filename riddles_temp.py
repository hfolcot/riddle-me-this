
def get_all_riddles(riddle_file):
    """
    Load the riddles from the txt file
    """
    with open(riddle_file) as f:
        riddles = f.read()
    print(riddles)
    