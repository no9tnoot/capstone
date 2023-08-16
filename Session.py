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
        self.details = []
        Session.readDatabaseDetails(self)
        #load database with details read from file
        self.database = self.loadDatabase(self.details[0],self.details[1],self.details[2],self.details[3])
        self.seed = Session.genSeed()
        self.user = user
        self.marker = Marker.Marker(self.database)
    
    #create instance of database with default parameters
    def loadDatabase(self, host='localhost', user='root', pword='mySQL_sew1', db_name = 'classicmodels2022'):
        return Database.Database(host, user, pword, db_name)
    
    #create instance of database with default parameters
    #def loadDatabase(self, host, user, pword, db_name):
        #return Database.Database(host, user, pword, db_name)
    
    # #generate seed from datetime
    # def genSeed():
    #     return int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    
    # #generate seed from date, for tests
    # def genTestSeed():
    #     return int(datetime.date.now().strftime("%Y%m%d"))
    
    #generate an easy question
    def genQuestion(self):
        return Question.EasyQuestion(self.database, self.seed)
    
    def  markQuery(self, stuAns,  modalAns):
        return self.marker.markQuery(stuAns, modalAns)
    
    #reads line by line from file in order: host, user, password, database name
    def readDatabaseDetails(self):
        f = open('database_details.txt','r')
        for x in f:
            self.details.append(x.strip())
    
    
    #create a quiz with the chosen database, a distribution of easy/medium/hard questions, and whether it is a test or not
        #maybe change depending on how we want to implements tests
    #def genQuiz(self, database, distribution = [10, 10, 10], test = False):
        #Quiz.Quiz(self, database, distribution, test)
