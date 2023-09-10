# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# Query Factory

import ISQLQuery
from EasySQLQuery import EasySQLQuery
#import MediumSQLQuery
#import HardSQLQuery
from EasyEnglishQuery import EasyEnglishQuery
#import MediumEnglishQuery
#import HardEnglishQuery
import Question

class QuestionFactory:
    
    def __init__(self, database):
        #self.question
        self.database = database
        
    
    def getQuestion(self, difficulty):
        match difficulty:
            case 'easy':
                sqlQuery = EasySQLQuery(self.database, 'seed')
                engQuery = EasyEnglishQuery(sqlQuery.getDict())
            
            case 'medium':
                sqlQuery = MediumSQLQuery(self.database)
                engQuery = MediumEnglishQuery(sqlQuery)
            
            case 'hard':
                sqlQuery = HardSQLQuery(self.database)
                engQuery = HardEnglishQuery(sqlQuery)
            
        self.question = Question(sqlQuery, engQuery)
        return self.question
    
#testing
from Session import Session
d = Session.loadDatabase()
factory = QuestionFactory(d)
q = factory.getQuestion('easy')
print(q.getSqlQuery())
print(q.getEnglishQuery())
                