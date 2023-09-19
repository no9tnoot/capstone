# Sian Wood
# 13/09/2023
# Flask: web pages for testSQL capstone

from flask import Flask, render_template, request
from QuizSetup import QuizSetup
from Session import Session

from test_login import check_login_details #, get_eng
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
    
    questionList = list(questionSet)
    for i in range(int(0.2*numQs)):
        # questionList.append(factory.getQuestion("hard"))
        questionList.append("Hard question here")

    return questionList

# Login page:
@app.route("/", methods=["GET", "POST"])
def login():
    #print(request.args)
    #print(request.form.get("username"))
    if request.method == "POST":
        #print(request.form.get("username"))
        # If the username and password are valid, return home page
        if check_login_details(request.form.get("username"), request.form.get("password")):
            return render_template("home_gui.html")
        else:
            return """
                <h1>Invalid login details</h1>
                <a href="/">back to login</a>
                """
    return render_template("login_gui.html")

# Home page:
@app.route("/home", methods=["GET", "POST"])
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

            if setup.result[0] == False:
                setup.result[2] = "The model output for this query was \"" + modelSQL + ";\" You inputted \"" + stuSQL + "\""

            setup.marked = True # Set flag
            print("Press mark: " + str(setup.marked))

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
            print("Change difficulty: " + str(setup.marked))
            return setup.question.getEnglishQuery() # Return Eng query of question

    
    # Render a practice page which displays the generated English query
    return render_template("practice_gui.html", engQuestion=setup.question.getEnglishQuery(), correct = setup.result[0], explanation = setup.result[1], model = setup.result[2], showResult = setup.marked) 

# Test quiz page:
@app.route("/test", methods=["GET", "POST"])
def test():
    numQs = 10 # Must be divisible by 10

    # If the questions have not yet been generated
    if not setup.questionList:
        print("List empty.")
        # Generate questions
        setup.questionList = genTestQs(numQs)

    if request.method == "POST":
        
        if "mark_button" in request.form:
            # Mark the student's inputted SQL query
            correctAns = []
            for i in range(numQs):
                stuAns = request.form.get("sql" + str(i))
                if stuAns == None:
                    stuAns = ""
                modelAns = setup.questionList[i].getSqlQuery()
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
            print(str(counter) + "/" + str(numQs))
 
    return render_template("test_gui.html", engE1 = setup.questionList[0].getEnglishQuery(), 
                            engE2 = setup.questionList[1].getEnglishQuery(), engE3 = setup.questionList[2].getEnglishQuery(), 
                            engM1 = setup.questionList[3].getEnglishQuery(), engM2 = setup.questionList[4].getEnglishQuery(), 
                            engM3 = setup.questionList[5].getEnglishQuery(), engM4 = setup.questionList[6].getEnglishQuery(), 
                            engM5 = setup.questionList[7].getEnglishQuery(), engH1 = setup.questionList[8], 
                            engH2 = setup.questionList[9])

# Statistics page:
@app.route("/statistics", methods=["GET", "POST"])
def stats():
    return """
    <h1>STATISTIC</h1>
    """
    print(request.form) 
    return render_template("stats_gui.html")

def main():
    global setup
    setup = QuizSetup()
    app.run()

if __name__ == "__main__":
    main()

