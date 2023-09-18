# Sian Wood
# 13/09/2023
# Flask: web pages for testSQL capstone

from flask import Flask, render_template, request
from Session import Session
from QuestionFactory import QuestionFactory

from test_login import check_login_details #, get_eng
app = Flask(__name__, template_folder="templates")

class flaskGUI():
    
    def __init__(self, session, factory):
        self.session = Session("user") # Create session
        db = session.database # Load the database
        self.factory = QuestionFactory(db) # Create the question factory

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
    def practice(self):

        # SETUP
        qLevel = "easy" # Set the initial question level to easy, and generate the first question
        question = self.factory.getQuestion(qLevel) # Generate the first question
        marked = False # Flag to indicate whether results should be showing

        if request.method == "POST":
            print(request.form)
            
            if "mark_button" in request.form:
                # Mark the student's inputted SQL query
                stuAns = request.form.get("sql") # Get student's input
                modelAns = self.session.getSqlQuery() # Get model answer
                mark = Session.markQuery(self.session, stuAns, modelAns) # Mark

                print(mark)

                marked = True # Set flag

                print("\"marked\" set to True. \n Results should be showing.")
            
            elif "next_button" in request.form:
                # Store question and results
                # Generate new question of selected difficulty level
                print("Next button pressed")

            elif "difficulty_changed" in request.form:
                qLevel = request.form.get("difficulty") # Get the new difficulty set by user -> update qLevel
                newQuestion = self.factory.getQuestion(qLevel) # Generate question
                return newQuestion.getEnglishQuery() # Return Eng query of question

        
        # Render a practice page which displays the generated English query
        return render_template("practice_gui.html", engQuestion=question.getEnglishQuery(), showResult = marked) 

    # Test quiz page:
    @app.route("/test", methods=["GET", "POST"])
    def test(self):

        # Generate questions
        easy1 = self.factory.getQuestion("easy") 
        easy2 = self.factory.getQuestion("easy")
        easy3 = self.factory.getQuestion("easy")
        med1 = self.factory.getQuestion("medium")
        med2 = self.factory.getQuestion("medium")
        med3 = self.factory.getQuestion("medium")
        med4 = self.factory.getQuestion("medium")
        med5 = self.factory.getQuestion("medium")
        hard1 = self.factory.getQuestion("hard")
        hard2 = self.factory.getQuestion("hard")

        print(request.form) 
        return render_template("test_gui.html", engE1 = easy1.getEnglishQuery(), engE2 = easy2.getEnglishQuery(), engE3 = easy3.getEnglishQuery(), engM1 = med1.getEnglishQuery(), engM2 = med2.getEnglishQuery(), engM3 = med3.getEnglishQuery(), engM4 = med4.getEnglishQuery(), engM5 = med5.getEnglishQuery(), engH1 = hard1.getEnglishQuery(), engH2 = hard2.getEnglishQuery())

    # Statistics page:
    @app.route("/statistics", methods=["GET", "POST"])
    def stats():
        return """
        <h1>STATISTIC</h1>
        """
        print(request.form) 
        return render_template("stats_gui.html")

    def main():
        app.run()

    if __name__ == "__main__":
        main()