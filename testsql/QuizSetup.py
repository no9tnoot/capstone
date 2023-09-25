# Sian Wood
# 18/09/2023
# QuizSetup class

from .Session import Session
from .QuestionFactory import QuestionFactory
from .Results import Results

class QuizSetup:
    """
    Class to set up all of the variables needed to store information while running the GUI.
    """

    def __init__(self):
        """
        Sets the session, database, factory, question level, question, marked, result and questionList
        instance variables for an instance of the QuizSetup class.
        """

        self.session = Session() # Create session
        self.db = self.session.database # Load the database
        self.factory = QuestionFactory(self.db) # Create the question factory
        self.qLevel = "easy" # Set the initial question level to easy, and generate the first question
        self.question = self.factory.getQuestion(self.qLevel) # Generate the first question
        self.marked = False # Flag to indicate whether results should be showing
        self.result = Results(True, "syn", "")
        self.questionList = []
        self.numQs = 10
        
    def __new__(setup):
        """
        Ensures that the Singleton design pattern is followed by only allowing the existence of a single
        instance of the QuizSetup class at one time.
        """

        if not hasattr(setup, 'instance'):
            setup.instance = super(QuizSetup, setup).__new__(setup)
        return setup.instance