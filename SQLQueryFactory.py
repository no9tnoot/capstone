# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# Query Factory

class SQLQueryFactory:
    
    def __init__(self):
        self.query
        
    
    def getSQLQuery(self, difficulty):
        match difficulty:
            case 'easy':
                self.query = 