# Sian Wood
# 13/09/2023
# Flask: web pages for testSQL capstone

from flask import Flask, render_template, request
from QuizSetup import QuizSetup
from Session import Session

from test_login import check_login_details #, get_eng
app = Flask(__name__, template_folder="templates")

def rmvDuplicates(arr):
    # Compare items in an array, ensuring that there are no duplicates
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j]:
                return i
    return -1


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
    print(setup.qLevel)

    if request.method == "POST":
        #print(request.form)
        
        if "mark_button" in request.form:
            # Mark the student's inputted SQL query
            modelSQL = setup.question.getSqlQuery()
            stuSQL = request.form.get("sql")
            setup.result = Session.markQuery(setup.session, stuSQL, modelSQL) # Mark
            # Change true to correct, false to incorrect

            if setup.result[0]:
                setup.result[0] = "Correct!"
            else:
                if setup.result[0] == False:
                    setup.result[2] = "The model output for this query was \"" + modelSQL + ";\" You inputted \"" + stuSQL + "\""
                setup.result[0] = "Incorrect"
            setup.marked = True # Set flag
        
        elif "next_button" in request.form:
            # Store question and results
            # Generate new question of selected difficulty level
            setup.question = setup.factory.getQuestion(setup.qLevel)
            setup.marked = False # Reset flag

        elif "difficulty_changed" in request.form:
            setup.qLevel = request.form.get("difficulty") # Get the new difficulty set by user -> update qLevel
            setup.question = setup.factory.getQuestion(setup.qLevel) # Generate question
            setup.marked = False # Reset flag
            return setup.question.getEnglishQuery() # Return Eng query of question

    
    # Render a practice page which displays the generated English query
    return render_template("practice_gui.html", engQuestion=setup.question.getEnglishQuery(), correct = setup.result[0], explanation = setup.result[1], model = setup.result[2], showResult = setup.marked) 

# Test quiz page:
@app.route("/test", methods=["GET", "POST"])
def test():
    numQs = 10 # Must be divisible by 10
    questionList = []

    # Generate questions
    for i in range(int(0.3*numQs)):
        # Generate 30% easy questions
        questionList.append(setup.factory.getQuestion("easy"))
        # Compare current question to previous questions
        for x in range(i-1):
            # If duplicate, replace
            if questionList[i] == questionList[x]:
                questionList[i] = setup.factory.getQuestion("easy")
            
    for i in range(int(0.5*numQs)):
        questionList.append(setup.factory.getQuestion("medium"))
    for i in range(int(0.2*numQs)):
        # questionList.append(factory.getQuestion("hard"))
        questionList.append("Hard question here")

    print(request.form) 
    return render_template("test_gui.html", engE1 = questionList[0].getEnglishQuery(), 
                            engE2 = questionList[1].getEnglishQuery(), engE3 = questionList[2].getEnglishQuery(), 
                            engM1 = questionList[3].getEnglishQuery(), engM2 = questionList[4].getEnglishQuery(), 
                            engM3 = questionList[5].getEnglishQuery(), engM4 = questionList[6].getEnglishQuery(), 
                            engM5 = questionList[7].getEnglishQuery(), engH1 = questionList[8], 
                            engH2 = questionList[9])

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

