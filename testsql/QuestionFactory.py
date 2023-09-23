# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# Query Factory

from .EasySQLQuery import EasySQLQuery
from .MediumSQLQuery import MediumSQLQuery
from .HardSQLQuery import HardSQLQuery
from .EasyEnglishQuery import EasyEnglishQuery
from .MediumEnglishQuery import MediumEnglishQuery
from .HardEnglishQuery import HardEnglishQuery
from .Question import Question

class QuestionFactory:
    
    def __init__(self, database):
        #self.question
        self.database = database
        
    
    def getQuestion(self, difficulty):
        match difficulty:
            case 'easy':
                sqlQuery = EasySQLQuery(self.database)
                engQuery = EasyEnglishQuery(sqlQuery.getDict())
            
            case 'medium':
                sqlQuery = MediumSQLQuery(self.database)
                engQuery = MediumEnglishQuery(sqlQuery.getDict())
            
            case 'hard':
                sqlQuery = HardSQLQuery(self.database)
                engQuery = HardEnglishQuery(sqlQuery.getDict())

            case _:
                print('Invalid difficulty')
            
        self.question = Question(sqlQuery.getSqlQuery(), engQuery.getEnglishQuery())
        return self.question
    
# #testing
if __name__ == "__main__":
    from Session import Session
    d = Session.loadDatabase()
    factory = QuestionFactory(d)
    q = factory.getQuestion('medium')
    print(q.getSqlQuery())
    print(q.getEnglishQuery())


                