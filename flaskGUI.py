# Sian Wood
# 13/09/2023
# Flask: web pages for testSQL capstone

from flask import Flask, render_template, request
from Session import Session
from QuestionFactory import QuestionFactory

from test_login import check_login_details #, get_eng

app = Flask(__name__, template_folder="templates")

# Login page:
@app.route("/", methods=["GET", "POST"])
def login():
    #print(request.args)
    print(request.form.get("username"))
    if request.method == "POST":
        print(request.form.get("username"))
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
    if request.method == "POST":
        print(request.form)
        
        if "mark_button" in request.form:
            # Mark the student's inputted SQL query
            stuAns = request.form.get("sql")
            modelAns = q.getSqlQuery()
            mark = Session.markQuery(s, stuAns, modelAns)
            print(mark)
        
        elif "next_button" in request.form:
            print("Next button pressed")

        elif "difficulty_changed" in request.form:
            c = factory.getQuestion(request.form.get("difficulty"))
            return c.getEnglishQuery()

    
    # Render a practice page which displays the generated English query
    return render_template("practice_gui.html", engQuestion=q.getEnglishQuery()) 

# Test quiz page:
@app.route("/test", methods=["GET", "POST"])
def test():
    return """
    <h1>TEST</h1>
    """
    print(request.form) 
    return render_template("test_gui.html")

# Statistics page:
@app.route("/statistics", methods=["GET", "POST"])
def stats():
    return """
    <h1>STATISTIC</h1>
    """
    print(request.form) 
    return render_template("stats_gui.html")


# Create session
s = Session("user")
# Load the database
d = s.database
# Create the question factory
factory = QuestionFactory(d)
# Set the initial question level to easy, and generate the first question
qLevel = "easy"
q = factory.getQuestion(qLevel)

app.run()

# #testing
# from Session import Session
# d = Session.loadDatabase()
# factory = QuestionFactory(d)
# q = factory.getQuestion('medium')
# print(q.getSqlQuery())
# print(q.getEnglishQuery())