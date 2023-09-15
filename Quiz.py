# Sian Wood
# 20 August 2023
# Quiz Class


import Session
import Question
from array import *

"""
Create a quiz object - either practice or a test - which will be associated with a student and 
displayed to that student
"""
class Quiz:
    
    def __init__(self, numEasy, numMed, numHard, user):
        self.difficultyDist = [numEasy,numMed,numHard]
        self.session = Session.Session(user)
        self.questions = []
    
    def generateQuestions(self, difficultyDist):
        #Generate easy questions and store in array
        for i in range(0,difficultyDist[0]-1,1):
            question = self.session.genEasyQuestion()
            self.questions.append([question.getQuery(), question.getQuestion()])
        
        #Generate medium questions and store in array
        for i in range(0, difficultyDist[1]-1, 1):
            question = self.session.genMedQuestion()
            self.questions.append([question.getQuery(), question.getQuestion()])

        #Generate hard questions and store in array
        for i in range(0, difficultyDist[2]-1, 1):
            question = self.session.genHardQuestion()
            self.questions.append([question.getQuery(), question.getQuestion()])
    