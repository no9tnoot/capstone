from .Session import Session
from .QuestionFactory import QuestionFactory

class QuizSetup:

    def __init__(self):
        # I don't think these all need to be instance vars. only the first 3?
        self.session = Session() # Create session
        self.db = self.session.database # Load the database
        self.factory = QuestionFactory(self.db) # Create the question factory
        self.qLevel = "easy" # Set the initial question level to easy, and generate the first question
        self.question = self.factory.getQuestion(self.qLevel) # Generate the first question
        self.marked = False # Flag to indicate whether results should be showing
        self.result = ["","",""]
        self.questionList = []
        self.engQsList = []
        
    def __new__(setup):
        if not hasattr(setup, 'instance'):
            setup.instance = super(QuizSetup, setup).__new__(setup)
        return setup.instance