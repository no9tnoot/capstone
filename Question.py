# Molly Ryan
# 7 August 2023
# Question Class


class Question:
    
    def __init__(self, database, seed):
        # get the attributes and their types from SQL, as well as the relations
        self.opperators = ['=', '<', '>', '<=', '>=', 'is', 'is not']
        self.aggregateFunctions = ['count()', 'max()', 'min()', 'avg()', '']
        self.condition = ['where', '']
        self.db = database
        self.seed = seed

 
class EasyQuestion(Question):
    
    def __init__(self):
        super().__init__()
        
        
class MediumQuestion(Question):
    
    def __init__(self):
        super().__init__()
        
        
class DifficultQuestion(Question):
    
    def __init__(self):
        super().__init__()