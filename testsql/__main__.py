# Sian Wood
# 13/09/2023
# Flask: web pages for testSQL capstone

from flask import Flask, render_template, request
from .QuizSetup import QuizSetup
from .Session import Session

app = Flask(__name__, template_folder="templates")

def addNonDuplicate(questions, difficulty):
    length = len(questions)
    while len(questions) == length:
        questions.add(setup.factory.getQuestion(difficulty))

def genTestQs(numQs):
    questionSet = set()
    # Check numQs multiple of 10

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
    return render_template("home_gui.html")

# Practice quiz page:
@app.route("/practice", methods=["GET", "POST"])
def practice():

    global setup
    # global result
    setup.marked = False
    print("Run practice: " + str(setup.marked))

    if request.method == "POST":
        
        if "mark_button" in request.form:
            # Mark the student's inputted SQL query
            modelSQL = setup.question.getSqlQuery()
            stuSQL = request.form.get("sql")
            setup.result = Session.markQuery(setup.session, stuSQL, modelSQL) # Mark
            # Change true to correct, false to incorrect

            #if setup.result[0] == False:
                #setup.result[2] = "The model output for this query was \"" + modelSQL + ";\" You inputted \"" + stuSQL + "\""

            setup.marked = True # Set flag
            # print("Press mark: " + str(setup.marked))

        elif "next_button" in request.form:
            # Store question and results
            # Generate new question of selected difficulty level
            setup.question = setup.factory.getQuestion(setup.qLevel)
            setup.marked = False # Reset flag
            print("Press next: " + str(setup.marked))

        elif "difficulty_changed" in request.form:
            setup.qLevel = request.form.get("difficulty") # Get the new difficulty set by user -> update qLevel
            setup.question = setup.factory.getQuestion(setup.qLevel) # Generate question
            setup.marked = False # Reset flag
            return setup.question.getEnglishQuery() # Return Eng query of question

    
    # Render a practice page which displays the generated English query
    try:
        stuSQL
    except NameError:
        stuSQL = ""
        
    return render_template("practice_gui.html", engQuestion=setup.question.getEnglishQuery(), correct = setup.result[0], explanation = setup.result[1], modelOutput = setup.result[2], showResult = setup.marked, difficulty = setup.qLevel, userQuery = stuSQL) 

# Test quiz page:
@app.route("/test", methods=["GET", "POST"])
def test():
    numQs = 20 # Must be divisible by 10

    # If the questions have not yet been generated
    if not setup.questionList:

        # Generate questions
        setup.questionList = genTestQs(numQs)

        # Just pass English queries to test_gui.py
        engQsList = []
        for i in range(numQs):
            engQsList.append(setup.questionList[i].getEnglishQuery())

    if request.method == "POST":
        
        if "mark_button" in request.form:
            # Mark the student's inputted SQL query
            correctAns = []

            for i in range(numQs):
                name = "sql" + str(i+1)
                print(name)
                stuAns = request.form.get(name) 

                print(stuAns)

                if stuAns == None:
                    stuAns = ""

                print(str(i))
                modelAns = setup.questionList[i].getSqlQuery()
                print(modelAns)
                setup.result = Session.markQuery(setup.session, stuAns, modelAns) # Mark

                # Store whether answer was correct or not
                correctAns.append(setup.result[0])
            
            # Count number of questions answered correctly
            counter = 0
            for i in correctAns:
                if i == True:
                    counter += 1
            
            # reset questionList
            setup.questionList = []
            mark = str(counter) + "/" + str(numQs)
            # Take to page with score and link to home
            return render_template("markedTest_gui.html", mark = mark)
 
    # Is this necessary?
    if engQsList is None:
        engQsList = []
    
    return render_template("test_gui.html", questions = engQsList, numQs = numQs)

def main():
    global setup
    setup = QuizSetup()
    app.run()

if __name__ == "__main__":
    main()

