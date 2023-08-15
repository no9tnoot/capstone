# Peter Berens
# 9 August 2023
# Session Class

import Database
#import Quiz
import datetime
import Question
import Marker

class Session:

    def __init__(self, user):
        self.database = self.loadDatabase()
        self.seed = Session.genSeed()
        self.user = user
        self.marker = Marker.Marker(self.database)
    
    #create instance of database with default parameters
    def loadDatabase(self):
        return Database.Database()
    
    #create instance of database with default parameters
    def loadDatabase(self, host, user, pword, db_name):
        return Database.Database(host, user, pword, db_name)
    
    #generate seed from datetime
    def genSeed():
        return int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    
    #generate seed from date, for tests
    def genTestSeed():
        return int(datetime.date.now().strftime("%Y%m%d"))
    
    def getQuestion(self):
        return Question.EasyQuestion(self.database, self.seed)
    
    
    #create a quiz with the chosen database, a distribution of easy/medium/hard questions, and whether it is a test or not
        #maybe change depending on how we want to implements tests
    #def genQuiz(self, database, distribution = [10, 10, 10], test = False):
        #Quiz.Quiz(self, database, distribution, test)
