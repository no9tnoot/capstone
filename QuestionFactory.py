# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# Query Factory

import ISQLQuery
import EasySQLQuery
import MediumSQLQuery
import HardSQLQuery

class QuestionFactory:
    
    def __init__(self):
        self.question
        
    
    def getQuestion(self, difficulty):
        match difficulty:
            case 'easy':
                sqlQuery = EasySQLQuery()
                engQuery = EasyEngQuery()
                self.question = Question(sqlQuery, engQuery)
                