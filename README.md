# Riddle Me This

View this project live at ...

A project completed in Python and Flask.

Test your lateral thinking skills by answering 20 riddles. 

The game will let individual players answer or skip each question and have their 
name entered into a high score table if they are in the top ten!

## UX

#### User Stories
•	As a teacher, I would like to test my class of 20 children on their multiplication 
tables, in order to see who still needs practice.

•	As an employer, I would like to pose riddles to job candidates in an interview, 
in order to see who is good at lateral thinking.

•	As a fan of quizzes, I would like to answer general knowledge questions, in 
order to see how my knowledge compares with that of others.

The planning stages of the Riddle Me This project have been documented in planning.docx 
which can be found in the main directory and will require MS Word or similar to view.

## Features

The game starts with a welcome page which allows users to read the game's instructions 
and enter a unique name before playing. The high score table is also available to 
view here.

They are then taken to the main game where a riddle is shown on the screen. The 
player has the choice to either attempt to answer the question or skip the question.
If they give a correct answer they are awarded a point and shown the next riddle. 
If an incorrect answer is given this is then printed underneath and they are permitted 
to try again. If the question is skipped they will be shown the next riddle but 
awarded no points. This will continue until all twenty questions have been attempted.

The player is then shown their result and the high score table shown with updated 
results, if applicable. The player is given the option to play again (go back to 
question 1) or end the game (logs the user out and returns to the welcome page).

### Features left to implement

No other features are currently planned.

## Technologies Used

* The main logic behind the game was written in [Python](https://www.python.org/)

* The project also uses the [Flask](http://flask.pocoo.org/) framework to enable 
HTML rendering and user sessions.

* The interface was created in [HTML](https://www.w3.org/html/) using [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
for styles. 

* Some styles from [Bootstrap](https://getbootstrap.com/) were also used for features such as the 
forms and high score table, and also for the grid layout.

## Testing

All of the main functions in the project are tested with unit testing in the file 
test_riddles.py. This can be run from the command line using `python3 -m unittest`

As all user stories are essentially the same, but requiring different questions, 
we will focus on the second: **As an employer, I would like to pose riddles to job candidates in an interview, 
in order to see who is good at lateral thinking.**

1. Welcome page
    * Try clicking Play without entering a username
    * Try giving a username with spaces
    * Try entering a username with unusual characters in eg. <>"
    * After playing the game through and then logging out and restarting, try entering the same username again.
2. Game page
    * Try clicking Go without entering an answer
    * Click on the Skip Question button and ensure the next question is displayed.
    * Enter an incorrect answer and click Go.
3. End page
    * Click on Play Again
    * Click on End Game

Google Chrome's developer tools have been used to test that the screen is displaying 
correctly at all screen sizes and on all devices available within the Tools function.

On testing I have noted the following issues:
* On using the username "test" and then trying to play again with the username "t",
I received an error saying the username had already been taken. This is caused by the if
statement checking to see if the name is in the list. **_Now fixed. The issue was caused by using read instead of readlines when opening the text file._**
* **Try clicking Go without entering an answer** - This will result in the page refreshing
and the username disappearing from the 'Good Luck (username)!' message.**_Now fixed. The issue was caused by a failure to pass the username through to the html page_**
* The high score table is rendering partially underneath the footer on mobile screens.

## Deployment

### Heroku


#### Questions

For reference, the questions can be updated as follows:

1. Ensure the questions are contained in a json file in the following format: 
    `{   
    "1": 
        {"question": "question 1", 
        "answer": "answer 1"}, 
    "2": 
        {"question": "question 2", 
        "answer": "answer 2"}}`
2. Update all instances of `get_data("data/riddles.json")` in run.py with the new file path.



## Credits

### Media

The 'question marks' background (qmarkbg.png) used in the header and footer were taken from [Pixabay.com](https://pixabay.com/en/question-mark-background-1909040/) (free)

The 'wood' background (bg.jpg) in the main body was from [Bestwallpapers.co](http://bestwallpapers.co/free-wallpapers-and-backgrounds/hd-backgrounds-free-ender-realtypark-co/) (free)

### Acknowledgements

The project was completed in order to fulfil the Milestone 3 project requirements 
for Code Institute's Full Stack Web Development Course. The idea for the game was 
outlined by Code Institute.
