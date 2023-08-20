# Molly Ryan, Sian Wood, Peter Berens
# 18 August 2023
# Question Class

class User:
    
    def getUserName():
        pass
    
    def checkPassword():
        pass
    

class Student(User):
    
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.results = []
        
    def getUserName(self):
        return self.name
    
    """Returns True if the entered password matches the recorded password, otherwise False."""
    def checkPassword(self, enteredPword):
        return (self.password==enteredPword)
    
    def saveResult(self, result):
        self.results.append(result)
        
    def getResults(self):
        return self.results
        
    

class Teacher(User):
    
    def __init__(self, name, password):
        self.name = name
        self.password = password
        
    def getUserName(self):
        return self.name
    
    """Returns True if the entered password matches the recorded password, otherwise False."""
    def checkPassword(self, enteredPword):
        return (self.password==enteredPword)
    
    def viewAllResults():
        #go get them results
        return # place holder