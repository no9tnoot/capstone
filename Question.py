# Molly Ryan, Peter Berens, Sian Wood
# 10 September 2023
# Question

class Question():

    def __init__(self, sqlQuery, engQuery):
        self.sqlQuery = sqlQuery
        self.engQuery = engQuery

    def getSqlQuery(self):
        return self.sqlQuery
    
    def getEnglishQuery(self):
        return self.engQuery