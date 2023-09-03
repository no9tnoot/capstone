# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# Query Factory

import ISQLQuery
import EasySQLQuery
import MediumSQLQuery
import HardSQLQuery
import EasyEnglishQuery
import MediumEnglishQuery
import HardEnglishQuery
import Question

class QuestionFactory:
    
    def __init__(self):
        self.question
        
    
    def getQuestion(self, difficulty):
        match difficulty:
            case 'easy':
                sqlQuery = EasySQLQuery()
                engQuery = EasyEnglishQuery()
            
            case 'medium':
                sqlQuery = MediumSQLQuery()
                engQuery = MediumEnglishQuery()
            
            case 'hard':
                sqlQuery = HardSQLQuery()
                engQuery = HardEnglishQuery()
            
        self.question = Question(sqlQuery, engQuery)
                