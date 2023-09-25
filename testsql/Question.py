# Molly Ryan, Peter Berens, Sian Wood
# 10 September 2023
# Question

class Question():
    """
    Question object simply hold an SQL query and the corresponding English question.
    """

    def __init__(self, sqlQuery, engQuery):
        self.sqlQuery = sqlQuery
        self.engQuery = engQuery

    def getSqlQuery(self):
        return self.sqlQuery
    
    def getEnglishQuery(self):
        return self.engQuery
    
    def __eq__(self, other):
        if type(other) != type(self): return False
        return self.sqlQuery == other.sqlQuery and self.engQuery == other.engQuery

    def __hash__(self):
        return hash((self.engQuery, self.sqlQuery))