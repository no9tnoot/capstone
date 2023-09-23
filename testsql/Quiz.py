# Sian Wood
# 20 August 2023
# Quiz Class


from . import Session
from array import *

class Quiz:
    """
    Create a quiz object - either practice or a test - which will be associated with a student and 
    displayed to that student
    """
    
    def __init__(self, numEasy, numMed, numHard, user):
        self.difficultyDist = [numEasy,numMed,numHard]
        self.session = Session.Session(user)
        # Array of numEasy, numMed and numHard Question objects
        self.questions = []
    
    def generateQuestions(self, difficultyDist):
        #Generate easy questions and store in array
        for i in range(0,difficultyDist[0]-1,1):
            question = self.session.genEasyQuestion()
            #Add question object to array
            self.questions.append(question)
            
        
        #Generate medium questions and store in array
        for i in range(0, difficultyDist[1]-1, 1):
            question = self.session.genMedQuestion()
            self.questions.append([question.getQuery(), question.getQuestion()])

        #Generate hard questions and store in array
        for i in range(0, difficultyDist[2]-1, 1):
            question = self.session.genHardQuestion()
            self.questions.append([question.getQuery(), question.getQuestion()])
    