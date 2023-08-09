# Peter Berens
# 9 August 2023
# Session Class

import Database
import Quiz
import datetime

class Session:
    def __init__(self, user):
        self.database = self.loadDatabase()
        self.seed = Session.genSeed()
        self.user = user
    
    #create instance of database with default parameters
    def loadDatabase(self):
        return Database.Database(host='localhost', user='root', pword='mySQL_sew1', db_name = 'classicmodels2022')
    
    #generate seed from datetime
    def genSeed():
        return int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    
    #create a quiz with the chosen database, a distribution of easy/medium/hard questions, and whether it is a test or not
        #maybe change depending on how we want to implements tests
    def genQuiz(self, database, distribution = [10, 10, 10], test = False):
        Quiz.Quiz(self, database, distribution, test)
