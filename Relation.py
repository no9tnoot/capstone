# Molly Ryan
# 8 August 2023
# Relation Class


class Relation:
    
    def __init__(self, n):
        self.name = n
        self.attributes=[]
        self.numAttributes=0
    
    def addAttribute(self, attribute):
        self.attributes.append(attribute)
        self.numAttributes=self.numAttributes+1
        
    def getAttribute(self, i):
        # check that the attribute number asked for is not out of bounds
        if (i<self.numAttributes):
            return self.attributes[i]
        else:
            return 0
        
    def getNumAttributes(self):
        return self.numAttributes