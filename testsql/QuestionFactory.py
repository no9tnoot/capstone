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
    """
    Factory for generating Question objects of varying difficulty. Generates the mySQL Query
    string, and the accompanying English version of the query, and passes them to the generated 
    question object.
    """
    
    def __init__(self, database):
        """
        Sets the database instance variable for the factory.
        """
        self.database = database
        
    
    def getQuestion(self, difficulty):
        """
        Generates and returns a runnable Question of the given difficulty.
        """
        # Generate a query that runs without producing errors. This catches errors thrown by
        # attributes with poor syntax (e.g. string values with reserved characters such as ' )
        finished = False
        while not finished: 
            try:
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
                finished = True
            except: pass
            
        self.question = Question(sqlQuery.getSqlQuery(), engQuery.getEnglishQuery())
        return self.question
    
# # #testing
# if __name__ == "__main__":
#     from Session import Session
#     d = Session.loadDatabase()
#     factory = QuestionFactory(d)
#     q = factory.getQuestion('medium')
#     print(q.getSqlQuery())
#     print(q.getEnglishQuery())


                