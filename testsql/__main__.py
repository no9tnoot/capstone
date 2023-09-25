# Sian Wood
# 13/09/2023
# Flask: web pages for testSQL capstone

from flask import Flask, render_template, request
from .QuizSetup import QuizSetup
from .Session import Session

app = Flask(__name__, template_folder="templates")

def addNonDuplicate(questions, difficulty):
    """Adds questions of the specified difficulty level to the questions set. Sets do not allow the addition
    of duplicate elements.
    """

    length = len(questions)
    while len(questions) == length: #While no questions have been added to the questions set
        questions.add(setup.factory.getQuestion(difficulty))

def genTestQs(numQs):
    """Creates a set, adds the correct proportion of easy, medium and hard questions to this set, and then 
    converts the set to a list and returns it.
    """

    questionSet = set()

    # Generate 30% easy questions
    for i in range(int(0.3*numQs)):
        addNonDuplicate(questionSet, "easy")
    for i in range(int(0.5*numQs)):
        addNonDuplicate(questionSet, "medium")
    for i in range(int(0.2*numQs)):
        addNonDuplicate(questionSet, "hard")
    
    questionList = list(questionSet)
    return questionList

# Home page:
@app.route("/", methods=["GET", "POST"])
def home():
    """Resets the question, marked and questionList variables of the current instance of QuizSetup, 
    and then renders the home page html.
    """

    setup.question = setup.factory.getQuestion(setup.qLevel)
    setup.marked = False # Reset flag
    setup.questionList = []
    return render_template("home_gui.html")

# Practice quiz page:
@app.route("/practice", methods=["GET", "POST"])
def practice():
    """Handles user interactions with the mark button, next button and with the difficulty selector, and 
    renders the practice page html.
    """

    global setup
    setup.marked = False # The current question has not been marked

    if request.method == "POST":
        
        if "mark_button" in request.form:
            modelSQL = setup.question.getSqlQuery()
            stuSQL = request.form.get("sql")
            setup.result = Session.markQuery(setup.session, stuSQL, modelSQL)  # Mark the student's inputted SQL query
            setup.marked = True                                                # The current question has been marked

        elif "next_button" in request.form:
            setup.question = setup.factory.getQuestion(setup.qLevel)           # Generate new question of selected difficulty level
            setup.marked = False                                               # The current question has not been marked

        elif "difficulty_changed" in request.form:
            setup.qLevel = request.form.get("difficulty")                      # Get the new difficulty set by user, and update qLevel
            setup.question = setup.factory.getQuestion(setup.qLevel)           # Generate new question of selected difficulty level
            setup.marked = False                                               # The current question has not been marked
            return setup.question.getEnglishQuery()                            # Return Eng query of question to javaScript in practice_gui.html
    
    # If stuSQL has not been allocated a value, set it as an empty string
    try:
        stuSQL
    except NameError:
        stuSQL = ""

    # Render a practice page which displays the generated English query
    # If not marked, it should provide space for the user to input their SQL query
    # If marked, the results should be displayed along with the expected SQL output
    return render_template("practice_gui.html", engQuestion=setup.question.getEnglishQuery(), correct = setup.result.correct, explanation = setup.result.comment, modelOutput = setup.result.tableInfo, showResult = setup.marked, difficulty = setup.qLevel, userQuery = stuSQL) 

# Select number of test questions page:
@app.route("/numQsSelect", methods=["GET", "POST"])
def numQsSelect():
    """Sets the number of questions to be generated for the test, and renders the numQsSelect page."""
    
    setup.numQs = 10 # Set to default

    if request.method == "POST" and "numQs_changed" in request.form:
            setup.numQs = int(request.form.get("numQs"))

    return render_template("numQsSelect_gui.html")


# Test quiz page:
@app.route("/test", methods=["GET", "POST"])
def test():
    """Generates a list of questions if one does not currently exist, handles user interactions with the 
    submit button, and renders the test page html.
    """

    if setup.questionList == []:              # If the questions have not yet been generated
        setup.questionList = genTestQs(setup.numQs) # Generate questions

        engQsList = []                        # Pass only the English queries to test_gui.py
        for i in range(len(setup.questionList)):
            engQsList.append(setup.questionList[i].getEnglishQuery())

    if request.method == "POST":
        if "mark_button" in request.form:     # Mark the student's inputted SQL query
            correctAns = []

            for i in range(len(setup.questionList)):                                                # For each question
                stuAns = request.form.get("sql" + str(i+1))                       # Get its model answer
                modelAns = setup.questionList[i].getSqlQuery()                    # Get the student's answer
                setup.result = Session.markQuery(setup.session, stuAns, modelAns) # Mark
                correctAns.append(setup.result.correct)                           # Store whether answer was correct or not
            
            counter = 0                      # Count number of questions answered correctly
            for i in correctAns:
                if i == True:
                    counter += 1
            
            setup.questionList = []          # Reset questionList
            mark = str(counter) + "/" + str(setup.numQs) 
            # Render page with student's score, a link to home, and a link to another test
            return render_template("markedTest_gui.html", mark = mark) 
    
    # If engQsList has not been allocated a value, set it as an empty string
    try:
        engQsList
    except NameError:
        engQsList = ""
    
    # Render a test page which displays the generated list of English questions
    return render_template("test_gui.html", questions = engQsList, numQs = setup.numQs)

def main():
    """Initialises the QuizSetup instance and runs the app
    """
    global setup
    setup = QuizSetup()
    app.run()

if __name__ == "__main__":
    main()

